from nicegui import ui
import insert
import sqlite3
import datetime
import random

# --- DATABASE CONFIG ---
DB = 'School_Results_Database.db'

# --- 1. DYNAMIC ANALYTICS LOGIC ---
def get_dashboard_metrics():
    try:
        with sqlite3.connect(DB) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute('SELECT * FROM academic_records').fetchall()
            if not rows: return None
            
            # Calculate Averages per Subject
            maths = [r['Maths'] for r in rows if r['Maths'] is not None]
            eng = [r['English'] for r in rows if r['English'] is not None]
            sst = [r['SST'] for r in rows if r['SST'] is not None]
            sci = [r['Science'] for r in rows if r['Science'] is not None]
            
            subs = {"Maths": sum(maths)/len(maths) if maths else 0,
                    "English": sum(eng)/len(eng) if eng else 0,
                    "SST": sum(sst)/len(sst) if sst else 0,
                    "Science": sum(sci)/len(sci) if sci else 0}
            
            # Find Best/Worst
            best_sub = max(subs, key=subs.get)
            worst_sub = min(subs, key=subs.get)
            
            # Calculate Class Average for Rising Stars
            all_avgs = [r['Average'] for r in rows if r['Average']]
            class_avg = sum(all_avgs) / len(all_avgs) if all_avgs else 0
            
            # Rising Stars: Above class average AND above 60
            rising_stars = [r for r in rows if r['Average'] > class_avg and r['Average'] > 60]
            
            # At Risk: Bottom 3 performers
            sorted_rows = sorted(rows, key=lambda x: x['Average'] or 0)
            at_risk = sorted_rows[:3]
            
            return {"best": best_sub, "worst": worst_sub, "at_risk": at_risk, "rising": rising_stars[:3]}
    except:
        return None

# --- 2. EDIT RECORD LOGIC ---
def edit_record(record, on_save):
    with ui.dialog() as dialog, ui.card().classes('w-[700px] p-8'):
        ui.label(f"Edit Record: {record['Name']}").classes('text-2xl font-bold mb-4')
        with ui.grid(columns=2).classes('w-full gap-4'):
            fields = {
                'Name': ui.input('Name', value=record['Name']),
                'Admin': ui.input('Admin', value=record['Admin']),
                'Class': ui.input('Class', value=record['Class']),
                'Maths': ui.number('Maths', value=record['Maths']),
                'English': ui.number('English', value=record['English']),
                'SST': ui.number('SST', value=record['SST']),
                'Science': ui.number('Science', value=record['Science']),
                'Remarks': ui.input('Remarks', value=record['Remarks'])
            }
        
        def save():
            with sqlite3.connect(DB) as conn:
                conn.execute('''UPDATE academic_records SET 
                    Name=?, Admin=?, Class=?, Maths=?, English=?, 
                    SST=?, Science=?, Remarks=? WHERE id=?''',
                    (fields['Name'].value, fields['Admin'].value, fields['Class'].value, 
                     fields['Maths'].value, fields['English'].value, fields['SST'].value, 
                     fields['Science'].value, fields['Remarks'].value, record['id']))
            ui.notify("Record updated successfully!", type='positive')
            dialog.close()
            on_save()
        
        ui.button('Save Changes', on_click=save).classes('w-full mt-6 bg-[#800000] text-white')
    dialog.open()

# --- 3. VIEW RECORDS TAB ---
def view_records_content():
    columns = [
        {'name': 'actions', 'label': 'Edit', 'field': 'actions', 'align': 'center'},
        {'name': 'Name', 'label': 'Name', 'field': 'Name', 'align': 'left'},
        {'name': 'Admin', 'label': 'Admin', 'field': 'Admin', 'align': 'center'},
        {'name': 'Class', 'label': 'Class', 'field': 'Class', 'align': 'center'},
        {'name': 'Maths', 'label': 'Maths', 'field': 'Maths', 'align': 'center'},
        {'name': 'English', 'label': 'English', 'field': 'English', 'align': 'center'},
        {'name': 'SST', 'label': 'SST', 'field': 'SST', 'align': 'center'},
        {'name': 'Science', 'label': 'Science', 'field': 'Science', 'align': 'center'},
        {'name': 'Total', 'label': 'Total', 'field': 'Total', 'align': 'center'},
        {'name': 'Grade', 'label': 'Grade', 'field': 'Grade', 'align': 'center'},
        {'name': 'Remarks', 'label': 'Remarks', 'field': 'Remarks', 'align': 'left'},
    ]
    content_area = ui.column().classes('w-full')

    def load_data():
        content_area.clear()
        with content_area:
            try:
                with sqlite3.connect(DB) as conn:
                    conn.row_factory = sqlite3.Row
                    all_rows = [dict(r) for r in conn.execute('SELECT * FROM academic_records').fetchall()]
                if not all_rows:
                    ui.label('No records found.').classes('text-gray-500 p-8')
                else:
                    student_table = ui.table(columns=columns, rows=all_rows, row_key='id').classes('w-full')
                    student_table.add_slot('body-cell-actions', '''
                        <q-td :props="props">
                            <q-btn icon="edit" flat dense color="primary" @click="$parent.$emit('edit', props.row)"></q-btn>
                        </q-td>
                    ''')
                    student_table.on('edit', lambda msg: edit_record(msg.args, load_data))
            except Exception as e:
                ui.label(f'Error: {e}')
    load_data()

# --- 4. STAFF HOME ---
def teacher():
    ui.query('.nicegui-content').classes('w-full min-h-screen bg-stone-50 p-8')
    
    verses = [
        "Train up a child in the way he should go... — Proverbs 22:6",
        "Let the children come to me... — Matthew 19:14",
        "For I know the plans I have for you... — Jeremiah 29:11",
        "I can do all things through Christ... — Philippians 4:13",
        "The Lord bless you and keep you... — Numbers 6:24",
        "Your word is a lamp to my feet... — Psalm 119:105",
        "Be strong and courageous... — Joshua 1:9",
        "Let your light shine before others... — Matthew 5:16",
        "The fruit of the Spirit is love, joy, peace... — Galatians 5:22",
        "Trust in the Lord with all your heart... — Proverbs 3:5",
        "Do your best to present yourself to God... — 2 Timothy 2:15",
        "Children are a heritage from the Lord... — Psalm 127:3",
        "The fear of the Lord is the beginning of wisdom... — Proverbs 9:10",
        "Whatever you do, work at it with all your heart... — Colossians 3:23",
        "The Lord is my light and my salvation... — Psalm 27:1",
        "For God has not given us a spirit of fear... — 2 Timothy 1:7",
        "Great are the works of the Lord... — Psalm 111:2",
        "May the Lord give you strength... — Psalm 29:11",
        "Love the Lord your God with all your heart... — Matthew 22:37",
        "The Lord is good to all... — Psalm 145:9",
        "Be kind to one another... — Ephesians 4:32",
        "Let everything you do be done in love... — 1 Corinthians 16:14",
        "I have loved you with an everlasting love... — Jeremiah 31:3",
        "For where your treasure is, there your heart will be... — Matthew 6:21",
        "The Lord will guide you always... — Isaiah 58:11",
        "Blessed are those who hunger and thirst for righteousness... — Matthew 5:6",
        "Commit to the Lord whatever you do... — Proverbs 16:3",
        "With God all things are possible... — Matthew 19:26",
        "Grow in the grace and knowledge of our Lord... — 2 Peter 3:18",
        "A cheerful heart is good medicine... — Proverbs 17:22"
    ]

    with ui.column().classes('w-full items-center'):
        with ui.column().classes('w-[95%] max-w-7xl gap-8'):
            
            # --- Header ---
            with ui.card().classes('w-full p-12 bg-white shadow-lg rounded-3xl text-center'):
                ui.label("Teacher's Dialogue").classes('text-5xl font-extrabold')
            
            # --- Daily Inspiration ---
            with ui.card().classes('w-full p-6 bg-amber-50 border-l-8 border-amber-400'):
                ui.label('📖 Daily Inspiration').classes('text-amber-900 font-bold text-sm')
                ui.label(random.choice(verses)).classes('text-amber-800 italic text-xl')
            
            # --- Tabs ---
            with ui.tabs().classes('w-full bg-white/80 backdrop-blur-md p-2 rounded-3xl shadow-xl border border-white/20') as tabs:
                tabs.classes('items-center justify-center')
                ui.tab('Dashboard', icon='dashboard').classes('rounded-2xl transition-all duration-300 hover:bg-[#800000]/10')
                ui.tab('Input Data', icon='add_circle').classes('rounded-2xl transition-all duration-300 hover:bg-[#800000]/10')
                ui.tab('View Records', icon='assignment').classes('rounded-2xl transition-all duration-300 hover:bg-[#800000]/10')
                ui.tab('Logout', icon='logout').classes('rounded-2xl transition-all duration-300 hover:bg-red-100 text-red-600')
        
            with ui.tab_panels(tabs, value='Dashboard').classes('w-full bg-transparent'):
                
                # --- Dashboard Panel ---
                with ui.tab_panel('Dashboard'):
                    metrics = get_dashboard_metrics()
                    with ui.row().classes('items-center mb-6'):
                            ui.icon('analytics', color='indigo', size='2rem')
                            ui.label('Performance Analytics').classes('text-2xl font-bold text-gray-800 ml-2')
                    
                    if metrics:
                        with ui.row().classes('w-full gap-6'):
                            # KPIs
                            with ui.card().classes('w-full md:w-1/3 p-6 shadow-sm border-t-4 border-t-indigo-500'):
                                ui.label('Subject Performance Trends').classes('text-sm font-semibold text-gray-500 mb-4')
                                with ui.row().classes('w-full justify-between'):
                                    with ui.column().classes('items-center'):
                                        ui.icon('trending_up', color='green', size='2rem')
                                        ui.label('Top').classes('text-xs text-gray-400 uppercase')
                                        ui.label(metrics['best']).classes('text-lg font-bold text-green-700')
                                    with ui.column().classes('items-center'):
                                        ui.icon('trending_down', color='red', size='2rem')
                                        ui.label('Low').classes('text-xs text-gray-400 uppercase')
                                        ui.label(metrics['worst']).classes('text-lg font-bold text-red-700')

                            # Support & Achievement Lists
                            with ui.card().classes('w-full md:w-[63%] p-6 shadow-sm'):
                                with ui.row().classes('w-full gap-8'):
                                    # Column 1: Academic Intervention
                                    with ui.column().classes('flex-1'):
                                        with ui.row().classes('items-center gap-2 mb-3'):
                                            ui.icon('warning_amber', color='red', size='1.5rem')
                                            ui.label('Academic Intervention').classes('text-sm font-bold text-red-800')
                                        for s in metrics['at_risk']:
                                            with ui.row().classes('w-full justify-between py-1 border-b border-gray-100'):
                                                ui.label(f"{s['Name']} ({s['Class']})").classes('text-sm')
                                                ui.label(f"{round(s['Average'] or 0, 1)}%").classes('font-mono text-xs text-red-600')

                                    # Column 2: Rising Stars
                                    with ui.column().classes('flex-1 bg-green-50 p-4 rounded shadow-sm border border-green-100'):
                                        with ui.row().classes('items-center gap-2 mb-3'):
                                            ui.icon('workspace_premium', color='green', size='1.5rem')
                                            ui.label('Rising Stars').classes('text-sm font-bold text-green-800')
                                        for s in metrics['rising']:
                                            with ui.row().classes('w-full justify-between py-1 border-b border-green-100'):
                                                ui.label(f"{s['Name']} ({s['Class']})").classes('text-sm')
                                                ui.label(f"{round(s['Average'] or 0, 1)}%").classes('font-mono text-xs text-green-600')
                    else:
                        with ui.card().classes('w-full p-10 items-center'):
                            ui.icon('analytics', size='3rem', color='grey')
                            ui.label('No academic data available for analysis.').classes('text-gray-500 mt-2')

                # --- Input Data Panel ---
                with ui.tab_panel('Input Data'):
                    with ui.card().classes('w-full p-6'):
                        insert.insert()

                # --- View Records Panel ---
                with ui.tab_panel('View Records'):
                    with ui.card().classes('w-full p-6'):
                        view_records_content()

                # --- Logout Panel ---
                with ui.tab_panel('Logout'):
                    with ui.card().classes('w-[300px] mx-auto items-center p-8'):
                        ui.icon('logout', size='4rem', color='red-500')
                        ui.label('Ready to leave?').classes('text-xl font-bold mt-4')
                        ui.label('Your session will be closed.').classes('text-gray-500 mb-6')
                        ui.button('Confirm Sign Out', color='red', on_click=lambda: ui.navigate.to('/')).classes('w-full')
