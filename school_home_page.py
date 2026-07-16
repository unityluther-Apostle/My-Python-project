import sqlite3
import io  # Added for CSV buffer
from nicegui import ui
import polars as pl
import insert
from datetime import datetime

ui.colors(primary='#800000', secondary='#ffffff', accent='#f59e0b')

student_records = []
all_records = []
student_table = None
DB = 'School_Results_Database.db'

# the block of code for downloading all the reports at once
def download_all_reports():
    if not all_records:
        ui.notify("No records to export", type='warning')
        return

    # We import the report function you already have
    import report

    # Generate all pages combined
    all_html = ""
    for record in all_records:
        # Get the individual report HTML and inject a page break
        single_report = report.report(record)
        all_html += f"<div style='page-break-after: always;'>{single_report}</div>"

    # Create a hidden dialog/window to hold the content and print
    ui.run_javascript(f'''
        const win = window.open('', '_blank');
        win.document.write(`{all_html}`);
        win.document.close();
        win.print();
    ''')
    ui.notify("Bulk report generation triggered", type='positive')


def local_calculate_grades(raw_data):
    def get_grade_expr(col):
        return pl.when(pl.col(col) >= 90).then(pl.lit("D1")) \
                  .when(pl.col(col) >= 80).then(pl.lit("D2")) \
                  .when(pl.col(col) >= 70).then(pl.lit("C3")) \
                  .when(pl.col(col) >= 60).then(pl.lit("C4")) \
                  .when(pl.col(col) >= 50).then(pl.lit("P5")) \
                  .when(pl.col(col) >= 40).then(pl.lit("P6")) \
                  .when(pl.col(col) >= 30).then(pl.lit("P7")) \
                  .otherwise(pl.lit("F9"))
    calc_df = pl.DataFrame([raw_data]).with_columns([
        get_grade_expr("Maths").alias("Maths_Grade"),
        get_grade_expr("English").alias("English_Grade"),
        get_grade_expr("SST").alias("SST_Grade"),
        get_grade_expr("Science").alias("Science_Grade"),
        (pl.col("Maths") + pl.col("English") + pl.col("SST") + pl.col("Science")).alias("Total"),
        ((pl.col("Maths") + pl.col("English") + pl.col("SST") + pl.col("Science")) / 4).alias("Average"),
    ]).with_columns([get_grade_expr("Average").alias("Grade"), pl.lit("N/A").alias("Rank")])
    return calc_df.to_dicts()[0]

def get_dashboard_stats():
    stats = {'total_students': 0, 'pass_rate': 0.0, 'subject_averages': {'Maths': 0, 'English': 0, 'SST': 0, 'Science': 0}, 'top_students': [], 'user_logs': []}
    try:
        with sqlite3.connect(DB) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) as count FROM academic_records")
            stats['total_students'] = cursor.fetchone()['count']
            if stats['total_students'] > 0:
                cursor.execute("SELECT COUNT(*) as passing FROM academic_records WHERE Grade != 'F'")
                stats['pass_rate'] = round((cursor.fetchone()['passing'] / stats['total_students']), 2)
            cursor.execute("SELECT AVG(Maths) as m, AVG(English) as e, AVG(SST) as sst, AVG(Science) as sci FROM academic_records")
            row = cursor.fetchone()
            if row and row['m'] is not None:
                stats['subject_averages'] = {'Maths': round(row['m'], 1), 'English': round(row['e'], 1), 'SST': round(row['sst'], 1), 'Science': round(row['sci'], 1)}

            cursor.execute("SELECT Name, Class, Total, Average, Grade, Rank, Maths, English, SST, Science FROM academic_records ORDER BY Total DESC LIMIT 3")
            stats['top_students'] = [dict(r) for r in cursor.fetchall()]

            cursor.execute('''
                SELECT username, timestamp, status,
                       (SELECT COUNT(*) FROM activity_logs al2 WHERE al2.username = activity_logs.username AND al2.id <= activity_logs.id AND al2.status='Active') as login_sequence
                FROM activity_logs
                ORDER BY id DESC
                LIMIT 5
            ''')
            stats['user_logs'] = [dict(r) for r in cursor.fetchall()]
    except Exception:
        pass
    return stats

def init_db_and_load_records():
    global student_records
    with sqlite3.connect(DB) as conn:
        cursor = conn.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS academic_records (id INTEGER PRIMARY KEY AUTOINCREMENT, Name TEXT, Admin TEXT, Class TEXT, ExamType TEXT, ExamDate TEXT, Attendance TEXT, Remarks TEXT, Maths INTEGER, Maths_Grade TEXT, English INTEGER, English_Grade TEXT, SST INTEGER, SST_Grade TEXT, Science INTEGER, Science_Grade TEXT, Total INTEGER, Average REAL, Grade TEXT, Rank TEXT)')

        try:
            cursor.execute("SELECT status FROM activity_logs LIMIT 1")
        except sqlite3.OperationalError:
            cursor.execute("DROP TABLE IF EXISTS activity_logs")

        cursor.execute('CREATE TABLE IF NOT EXISTS activity_logs (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, timestamp TEXT, status TEXT)')
        conn.commit()

def refresh_table_data(class_filter='All'):
    global student_table, all_records
    if student_table is None:
        return
    try:
        with sqlite3.connect(DB) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            if class_filter == 'All':
                cursor.execute("SELECT * FROM academic_records")
            else:
                cursor.execute("SELECT * FROM academic_records WHERE Class = ?", (class_filter,))

            all_records = [dict(r) for r in cursor.fetchall()]
            student_table.rows = all_records
            student_table.update()
    except Exception as e:
        ui.notify(f"Error loading records: {e}", type='negative')

def delete_record(record_id):
    try:
        with sqlite3.connect(DB) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM academic_records WHERE id = ?", (record_id,))
            conn.commit()
        ui.notify("Record removed successfully", type='positive')
        refresh_table_data()
    except Exception as e:
        ui.notify(f"Delete failed: {e}", type='negative')

def open_edit_dialog(record):
    with ui.dialog() as edit_dialog, ui.card().classes('w-[400px] p-6 gap-3'):
        ui.label(f"Edit Record: {record['Name']}").classes('text-lg font-bold text-slate-800')

        edit_name = ui.input('Name', value=record['Name']).classes('w-full')
        edit_class = ui.input('Class', value=record['Class']).classes('w-full')
        edit_maths = ui.number('Maths', value=record['Maths']).classes('w-full')
        edit_english = ui.number('English', value=record['English']).classes('w-full')
        edit_sst = ui.number('SST', value=record['SST']).classes('w-full')
        edit_science = ui.number('Science', value=record['Science']).classes('w-full')
        edit_rank = ui.input('Rank', value=record.get('Rank', 'N/A')).classes('w-full')

        def save_changes():
            raw_scores = {
                "Maths": int(edit_maths.value or 0),
                "English": int(edit_english.value or 0),
                "SST": int(edit_sst.value or 0),
                "Science": int(edit_science.value or 0)
            }
            updated_metrics = local_calculate_grades(raw_scores)

            try:
                with sqlite3.connect(DB) as conn:
                    cursor = conn.cursor()
                    cursor.execute('''
                        UPDATE academic_records SET
                            Name=?, Class=?, Maths=?, Maths_Grade=?,
                            English=?, English_Grade=?, SST=?, SST_Grade=?,
                            Science=?, Science_Grade=?, Total=?, Average=?, Grade=?, Rank=?
                        WHERE id=?
                    ''', (
                        edit_name.value, edit_class.value,
                        raw_scores['Maths'], updated_metrics['Maths_Grade'],
                        raw_scores['English'], updated_metrics['English_Grade'],
                        raw_scores['SST'], updated_metrics['SST_Grade'],
                        raw_scores['Science'], updated_metrics['Science_Grade'],
                        updated_metrics['Total'], updated_metrics['Average'], updated_metrics['Grade'],
                        edit_rank.value, record['id']
                    ))
                    conn.commit()
                ui.notify("Record updated successfully!", type='positive')
                edit_dialog.close()
                refresh_table_data()
            except Exception as e:
                ui.notify(f"Update failed: {e}", type='negative')

        with ui.row().classes('w-full justify-end gap-2 mt-4'):
            ui.button('Cancel', on_click=edit_dialog.close).props('flat')
            ui.button('Save', on_click=save_changes).props('unelevated color="primary"')

    edit_dialog.open()

def handle_logout():
    import loginPage
    current_user = loginPage.app_state.get('current_user', 'Admin')
    loginPage.update_login_activity(current_user, 'Logged Out')
    ui.notify('Logged out successfully', type='positive', color='#800000')
    ui.navigate.to('/login')

def home(client=None):
    global student_table
    ui.query('.q-page, .nicegui-content').style('max-width: none !important; width: 100% !important; padding: 0 !important;')
    ui.query('.nicegui-content').classes('w-full min-h-screen justify-center items-center flex bg-slate-50 p-4')

    dashboard_data = get_dashboard_stats()

    with ui.column().classes('w-full max-w-[95vw] xl:max-w-[85vw] gap-4'):
        with ui.card().classes('w-full p-2 bg-white shadow-md rounded-xl border border-slate-200').tight():
            with ui.row().classes('w-full items-center justify-between px-4 py-1'):
                with ui.row().classes('items-center gap-2'):
                    ui.icon('school', color='#800000').classes('text-2xl')
                    ui.label('AIM Pre-School').classes('text-lg font-bold text-slate-800')

                with ui.tabs().props('active-color="primary" indicator-color="primary" text-color="grey-7"') as nav_tabs:
                    home_tab = ui.tab('Home Dashboard', icon='dashboard')
                    teachers_tab = ui.tab('Entry Manager', icon='entry')
                    reports_tab = ui.tab('Academic Records', icon='assignment')
                    logout_tab = ui.tab('Log Out', icon='logout')

        starting_tab = home_tab

        with ui.tab_panels(nav_tabs, value=starting_tab).classes('w-full text-xl bg-transparent'):
            with ui.tab_panel(home_tab).classes('p-0 gap-4 flex flex-col'):
                with ui.card().classes('w-full p-6 bg-white shadow-lg rounded-2xl border border-slate-200'):
                    with ui.row().classes('w-full items-start no-wrap gap-4 mb-8'):
                        ui.image('https://images.unsplash.com/photo-1546410531-bb4caa6b424d?w=200') \
                            .classes('w-16 h-16 md:w-20 md:h-20 rounded-xl shadow-sm object-cover border border-slate-100 flex-shrink-0')

                        with ui.column().classes('flex-1 justify-center'):
                            ui.label("Administrator Dashboard") \
                                .classes('text-h4 md:text-h3 font-bold').style('color: #800000 !important; line-height: 1.2;')

                            with ui.row().classes('items-center gap-2 mt-1'):
                                ui.label(f"System Status: Operational | {datetime.now().strftime('%A, %B %d, %Y')}") \
                                    .classes('text-slate-500 text-sm font-medium')

                                ui.label('Centralized oversight for student academic progression, enrollment demographics, and instructor management systems.') \
                                    .classes('text-slate-400 text-xs mt-1')

                    # --- KPI Summary Row ---
                    with ui.row().classes('w-full gap-4 items-stretch mb-8'):
                        # Total Enrollment Card
                        with ui.card().classes('flex-1 p-4 bg-white shadow-md rounded-2xl border border-slate-200'):
                            with ui.row().classes('items-center gap-2'):
                                ui.icon('group', color='primary').classes('text-lg')
                                ui.label('Total Enrollment').classes('text-xs font-bold uppercase text-slate-400')
                            ui.label(str(dashboard_data.get('total_students', 0))).classes('text-3xl font-extrabold text-slate-800 mt-2')
                            ui.label('Active Student Records').classes('text-xs font-semibold text-slate-500 mt-1')

                        # Primary Classes Card
                        with ui.card().classes('flex-1 p-4 bg-white shadow-md rounded-2xl border border-slate-200'):
                            with ui.row().classes('items-center gap-2'):
                                ui.icon('school', color='primary').classes('text-lg')
                                ui.label('Primary Classes').classes('text-xs font-bold uppercase text-slate-400')
                            ui.label('P1 - P7').classes('text-3xl font-extrabold text-slate-800 mt-2')
                            ui.label('Managing controlled classroom environments.').classes('text-xs font-semibold text-slate-500 mt-1')

                        # Success Rate Card
                        with ui.card().classes('flex-1 p-4 bg-white shadow-md rounded-2xl border border-slate-200'):
                            with ui.row().classes('items-center gap-2'):
                                ui.icon('trending_up', color='primary').classes('text-lg')
                                ui.label('Aggregate Success Rate').classes('text-xs font-bold uppercase text-slate-400')

                            perc = dashboard_data.get('pass_rate', 0) * 100
                            percentage = round(perc, 1)
                            status = "Optimal" if percentage >= 85 else "Satisfactory" if percentage >= 70 else "Needs Review"
                            ui.label(f"{percentage}%").classes('text-3xl font-extrabold text-slate-800 mt-2')
                            ui.label(f"Performance Level: {status}").classes('text-xs font-semibold text-slate-500 mt-1')

                    # --- Detailed Analytics Row ---
                    with ui.row().classes('w-full gap-4 items-stretch justify-center'):
                        # Subject Averages Card
                        with ui.card().classes('w-full max-w-[500px] p-5 bg-white shadow-md rounded-2xl border border-slate-200'):
                            ui.label('Subject Averages').classes('text-base font-bold text-slate-800 mb-4')
                            for sub, val in dashboard_data.get('subject_averages', {}).items():
                                with ui.column().classes('w-full gap-1 mb-3'):
                                    with ui.row().classes('w-full justify-between items-center'):
                                        ui.label(sub).classes('text-xs font-semibold text-slate-600')
                                        ui.label(f"{val}%").classes('text-xs font-bold text-slate-800')
                                    ui.linear_progress(value=val/100 if val > 0 else 0.05, color='primary').classes('w-full rounded-sm')

                        # Top Performers Card
                        with ui.card().classes('w-full max-w-[500px] p-5 bg-white shadow-md rounded-2xl border border-slate-200'):
                            with ui.row().classes('items-center gap-2 mb-4'):
                                ui.icon('emoji_events', color='amber-7').classes('text-xl')
                                ui.label('Top Academic Performers').classes('text-base font-bold text-slate-800')

                            for idx, stud in enumerate(dashboard_data.get('top_students', [])):
                                # Safely define subjects for max() calculation
                                subs = {s: stud.get(s, 0) for s in ['Maths', 'English', 'SST', 'Science']}
                                best_sub = max(subs, key=subs.get)

                                with ui.row().classes('w-full items-center justify-between py-2 border-b border-slate-50 last:border-none'):
                                    ui.label(f"{idx+1}. {stud.get('Name', 'Unknown')}").classes('text-sm font-bold text-slate-800')
                                    ui.badge(f"{best_sub}: {stud.get(best_sub, 0)}", color='emerald-50') \
                                        .classes('text-emerald-700 font-bold text-[10px]')

            with ui.tab_panel(teachers_tab).classes('p-0 gap-4 flex flex-col'):
                with ui.card().classes('w-full p-6 bg-white shadow-md rounded-xl border border-slate-200'):
                    with ui.row().classes('w-full items-center justify-between'):
                        ui.label('Marks entry manager').classes('text-lg font-bold text-slate-800')
                        with ui.row().classes('gap-2 items-center'):
                            launch_btn = ui.button('Run Insert Function', icon='add_circle').props('color="primary" unelevated')
                            minimize_btn = ui.button('Minimize', icon='keyboard_arrow_up').props('color="grey-7" flat dense')
                    form_container = ui.column().classes('w-full gap-4 transition-all duration-300')
                    form_container.set_visibility(False)
                    launch_btn.on_click(lambda: (form_container.set_visibility(True), form_container.clear(), exec('with form_container: insert.insert()')))
                    minimize_btn.on_click(lambda: form_container.set_visibility(False))

            with ui.tab_panel(reports_tab).classes('p-0 gap-4 flex flex-col'):
                with ui.card().classes('w-full p-6 bg-white shadow-md rounded-xl border border-slate-200 flex flex-col gap-4'):
                    with ui.row().classes('w-full justify-between items-center'):
                        ui.label('Academic Records Database').classes('text-lg font-bold text-slate-800')

                        # --- ADDED CLASS FILTER DROPDOWN ---
                        class_select = ui.select(
                            ['All', 'P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7'],
                            value='All',
                            label='Filter by Class',
                            on_change=lambda e: refresh_table_data(e.value)
                        ).props('dense outlined').classes('w-32')

                        with ui.row().classes('items-center gap-2'):
                            # Pass the current filter value to export_csv if you want to export only filtered data
                            def export_csv():
                                if not all_records:
                                    ui.notify("No data to export", type='warning')
                                    return
                                df = pl.DataFrame(all_records)
                                buffer = io.StringIO()
                                df.write_csv(buffer)
                                ui.download(src=buffer.getvalue().encode('utf-8'), filename='student_records.csv')
                                ui.notify("Download started", type='positive')

                            search_input = ui.input(placeholder='Search student name...').props('dense outlined clearable')
                            ui.button(icon='search', on_click=lambda: apply_filter(search_input.value)).props('dense color="primary"')
                            ui.button('Export CSV', icon='download', on_click=export_csv).props('flat dense color="primary"')
                            ui.button('Refresh', icon='refresh', on_click=lambda: refresh_table_data(class_select.value)).props('outline dense text-color="primary"')
                            #ui.button('Print All', icon='print', on_click=download_all_reports).props('flat dense color="primary"')

                    columns = [
                        {'name': 'Name', 'label': 'Student', 'field': 'Name', 'align': 'left', 'sortable': True},
                        {'name': 'Class', 'label': 'Class', 'field': 'Class', 'align': 'center'},
                        {'name': 'Maths', 'label': 'Maths', 'field': 'Maths', 'align': 'center'},
                        {'name': 'Maths_Grade', 'label': 'M. Grade', 'field': 'Maths_Grade', 'align': 'center'},
                        {'name': 'English', 'label': 'English', 'field': 'English', 'align': 'center'},
                        {'name': 'English_Grade', 'label': 'E. Grade', 'field': 'English_Grade', 'align': 'center'},
                        {'name': 'SST', 'label': 'SST', 'field': 'SST', 'align': 'center'},
                        {'name': 'SST_Grade', 'label': 'SST Grade', 'field': 'SST_Grade', 'align': 'center'},
                        {'name': 'Science', 'label': 'Science', 'field': 'Science', 'align': 'center'},
                        {'name': 'Science_Grade', 'label': 'Sci. Grade', 'field': 'Science_Grade', 'align': 'center'},
                        {'name': 'Total', 'label': 'Total', 'field': 'Total', 'sortable': True, 'align': 'center'},
                        {'name': 'Grade', 'label': 'Final Grade', 'field': 'Grade', 'align': 'center'},
                        {'name': 'Rank', 'label': 'Rank', 'field': 'Rank', 'align': 'center', 'sortable': True},
                        {'name': 'actions', 'label': 'Actions', 'field': 'actions', 'align': 'center'}
                    ]
                
                    student_table = ui.table(columns=columns, rows=[], row_key='id').classes('w-full shadow-inner border border-slate-100')
                    ui.button('Print All', icon='print', on_click=download_all_reports).props('flat dense color="primary"')
                    student_table.add_slot('body-cell-Grade', '''
                        <q-td :props="props">
                            <q-badge :color="['D', 'E', 'F'].includes(props.value) ? 'red' : 'green'">
                                {{ props.value }}
                            </q-badge>
                        </q-td>
                    ''')

                    student_table.add_slot('body-cell-actions', '''
                        <q-td :props="props">
                            <q-btn flat dense round icon="edit" color="blue-7" @click="$parent.$emit('edit_row', props.row)"></q-btn>
                            <q-btn flat dense round icon="delete" color="red-7" @click="$parent.$emit('delete_row', props.row.id)"></q-btn>
                        </q-td>
                    ''')

                    student_table.on('edit_row', lambda msg: open_edit_dialog(msg.args))
                    student_table.on('delete_row', lambda msg: delete_record(msg.args))

                    refresh_table_data()

            with ui.tab_panel(logout_tab).classes('p-0 justify-center items-center flex min-h-[40vh]'):
                with ui.card().classes('w-full max-w-md p-8 text-center items-center flex flex-col gap-4'):
                    ui.icon('power_settings_new', color='#800000').classes('text-5xl bg-red-50 p-4 rounded-full')
                    ui.label('Confirm Sign Out').classes('text-xl font-bold text-slate-800')
                    with ui.row().classes('w-full gap-3 mt-2 justify-center'):
                        ui.button('Yes, Log Me Out', icon='logout', on_click=handle_logout).props('color="primary" unelevated')
                        ui.button('Cancel', on_click=lambda: nav_tabs.set_value(starting_tab)).props('color="grey-7" outline')

# this code helps to make the final grade display GRADE NOT final average
# Optional: Run this once to fix existing records if they show numbers
with sqlite3.connect(DB) as conn:
    cursor = conn.cursor()
    # This fetches rows and recalculates the grade for every existing record
    cursor.execute("SELECT id, Maths, English, SST, Science FROM academic_records")
    for row in cursor.fetchall():
        record_dict = dict(zip(['id', 'Maths', 'English', 'SST', 'Science'], row))
        metrics = local_calculate_grades(record_dict)
        cursor.execute("UPDATE academic_records SET Grade=? WHERE id=?", (metrics['Grade'], record_dict['id']))
    conn.commit()

import polars as pl

#this ensures that the ranks of different classes are preversed 
def update_all_ranks():
    with sqlite3.connect(DB) as conn:
        # Load all records into a Polars DataFrame
        df = pl.read_database("SELECT * FROM academic_records", conn)
        
        # Rank within each class
        # We sort by Class and then by Total descending
        df = df.with_columns(
            pl.col("Total").rank(descending=True, method="dense").over("Class").alias("Rank")
        )
        
        # Push the updated ranks back to the database
        # For a small/medium DB, converting to dicts and updating is fine:
        cursor = conn.cursor()
        for row in df.to_dicts():
            cursor.execute("UPDATE academic_records SET Rank = ? WHERE id = ?", (row['Rank'], row['id']))
        conn.commit()

#this is for the search by name
def apply_filter(query):
    global student_table, all_records
    if not query:
        student_table.rows = all_records
    else:
        # Ensure 'Name' exists in your dictionary keys
        student_table.rows = [r for r in all_records if query.lower() in r['Name'].lower()]
    student_table.update()
init_db_and_load_records()
