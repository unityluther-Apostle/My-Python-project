import sqlite3
from nicegui import ui
import polars as pl
import report  # Ensure report.py is in the same directory

DB = 'School_Results_Database.db'

# --- 1. DATABASE SETUP & MIGRATION ---
def migrate_db():
    with sqlite3.connect(DB) as conn:
        cursor = conn.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS academic_records (id INTEGER PRIMARY KEY AUTOINCREMENT)')
        
        required_columns = {
            "Name": "TEXT", "Admin": "TEXT", "Class": "TEXT", "ExamType": "TEXT", 
            "ExamDate": "TEXT", "Attendance": "TEXT", "Remarks": "TEXT", 
            "Maths": "INTEGER", "Maths_Grade": "TEXT", "English": "INTEGER", 
            "English_Grade": "TEXT", "SST": "INTEGER", "SST_Grade": "TEXT", 
            "Science": "INTEGER", "Science_Grade": "TEXT", "Total": "INTEGER", 
            "Average": "REAL", "Grade": "TEXT", "Rank": "INTEGER DEFAULT 0", 
            "Term": "INTEGER", "AcademicYear": "INTEGER", "FeesBalance": "REAL", 
            "ClassTeacherRemarks": "TEXT", "HeadteacherRemarks": "TEXT"
        }
        
        for col, col_type in required_columns.items():
            try:
                cursor.execute(f'ALTER TABLE academic_records ADD COLUMN {col} {col_type}')
            except sqlite3.OperationalError:
                pass 
        conn.commit()

# --- 2. THE INSERT UI FUNCTION ---
def insert():
    migrate_db() 

    def get_grade(score):
        if score is None: return "F9"
        if score >= 90: return "D1"
        if score >= 80: return "D2"
        if score >= 70: return "C3"
        if score >= 60: return "C4"
        if score >= 50: return "C5"
        if score >= 45: return "C6"
        if score >= 40: return "P7"
        if score >= 35: return "P8"
        return "F9"

    def save():
        for key, field in inputs.items():
            if field.value is None or (isinstance(field.value, str) and not field.value.strip()):
                ui.notify(f"Field {key} is required", type='warning')
                return

        payload = {k: v.value for k, v in inputs.items()}
        df = pl.DataFrame([payload])
        
        df = df.with_columns([
            pl.col("Maths").map_elements(get_grade, return_dtype=pl.String).alias("Maths_Grade"),
            pl.col("English").map_elements(get_grade, return_dtype=pl.String).alias("English_Grade"),
            pl.col("SST").map_elements(get_grade, return_dtype=pl.String).alias("SST_Grade"),
            pl.col("Science").map_elements(get_grade, return_dtype=pl.String).alias("Science_Grade"),
            (pl.col("Maths") + pl.col("English") + pl.col("SST") + pl.col("Science")).alias("Total")
        ]).with_columns(
            (pl.col("Total") / 4).alias("Average")
        ).with_columns(
            pl.col("Average").map_elements(lambda x: f"{round(x, 1)}", return_dtype=pl.String).alias("Grade")
        )
        
        row = df.to_dicts()[0]
        
        with sqlite3.connect(DB) as conn:
            conn.execute('''INSERT INTO academic_records 
                (Name, Admin, Class, ExamType, ExamDate, Attendance, Remarks, Maths, Maths_Grade, 
                 English, English_Grade, SST, SST_Grade, Science, Science_Grade, Total, Average, 
                 Grade, Rank, Term, AcademicYear, FeesBalance, ClassTeacherRemarks, HeadteacherRemarks) 
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', 
                (row['Name'], row['Admin'], row['Class'], row['ExamType'], row['ExamDate'], 
                 row['Attendance'], row['Remarks'], row['Maths'], row['Maths_Grade'], 
                 row['English'], row['English_Grade'], row['SST'], row['SST_Grade'], 
                 row['Science'], row['Science_Grade'], row['Total'], row['Average'], 
                 row['Grade'], 0, row['Term'], row['AcademicYear'], 
                 row['FeesBalance'], row['ClassTeacherRemarks'], row['HeadteacherRemarks']))
            
            cursor = conn.execute('SELECT id FROM academic_records WHERE Class = ? ORDER BY Average DESC', (row['Class'],))
            for rank_val, (student_id,) in enumerate(cursor.fetchall(), start=1):
                conn.execute('UPDATE academic_records SET Rank = ? WHERE id = ?', (rank_val, student_id))
            conn.commit()

        ui.notify(f"Record saved for {row['Name']}!", type='positive')
        load_table()

    def load_table():
        with sqlite3.connect(DB) as conn:
            conn.row_factory = sqlite3.Row
            rows = [dict(r) for r in conn.execute('SELECT * FROM academic_records ORDER BY Rank ASC').fetchall()]
            student_table.rows = rows
        student_table.update()

    # --- UI LAYOUT ---
    ui.query('body').classes('bg-gray-100')
    inputs = {}
    with ui.column().classes('w-full max-w-7xl mx-auto p-6 items-center'):
        ui.label("Teacher's Portal").classes('text-4xl font-black text-[#800000] mb-8')
        with ui.row().classes('w-full gap-8 justify-center items-start'):
            with ui.card().classes('w-full max-w-md p-6 bg-white border-t-8 border-[#800000] shadow-xl'):
                ui.label("Student Assessment Entry").classes('text-lg font-bold text-gray-700 mb-4')
                inputs['Name'] = ui.input("Student Name").classes('w-full').props('outlined dense')
                inputs['Admin'] = ui.input('Admission No.').classes('w-full').props('outlined dense')
                inputs['Class'] = ui.select(['P1','P2','P3','P4','P5','P6', 'P7'], label='Class').classes('w-full').props('outlined dense')
                with ui.grid(columns=3).classes('w-full gap-2 mt-2'):
                    inputs['Term'] = ui.select([1, 2, 3], label='Term').props('outlined dense')
                    inputs['AcademicYear'] = ui.input('Year', value='2026').props('outlined dense')
                    inputs['FeesBalance'] = ui.number('Fees Bal (UGX)', value=0).props('outlined dense')
                with ui.grid(columns=2).classes('w-full gap-2 mt-4'):
                    inputs['Maths'] = ui.number('Maths', min=0, max=100).props('outlined dense')
                    inputs['English'] = ui.number('English', min=0, max=100).props('outlined dense')
                    inputs['SST'] = ui.number('SST', min=0, max=100).props('outlined dense')
                    inputs['Science'] = ui.number('Science', min=0, max=100).props('outlined dense')
                inputs['ExamType'] = ui.select(['Beginning', 'Mid-Term', 'End-Term', 'Tests'], label='Exam Type').classes('w-full mt-2').props('outlined dense')
                inputs['ExamDate'] = ui.input('Date (dd/mm/yyyy)').classes('w-full').props('outlined dense')
                inputs['Attendance'] = ui.input('Attendance').classes('w-full').props('outlined dense')
                inputs['Remarks'] = ui.textarea('General Remarks').classes('w-full mt-2').props('outlined dense')
                inputs['ClassTeacherRemarks'] = ui.input('Class Teacher Remarks').classes('w-full mt-2').props('outlined dense')
                inputs['HeadteacherRemarks'] = ui.input('Head Teacher Remarks').classes('w-full mt-2').props('outlined dense')
                ui.button('Save Student Record', on_click=save).classes('w-full mt-6 bg-[#800000] text-white py-3 font-bold')

            with ui.card().classes('w-full max-w-4xl p-6 bg-white shadow-lg'):
                ui.label("Student Records Database").classes('text-lg font-bold text-gray-700 mb-4')
                student_table = ui.table(columns=[
                    
                    {'name': 'Rank', 'label': 'Rank', 'field': 'Rank'},
                    {'name': 'Name', 'label': 'Name', 'field': 'Name'},
                    {'name': 'Class', 'label': 'Class', 'field': 'Class'},
                    {'name': 'Average', 'label': 'Avg', 'field': 'Average'},
                    {'name': 'actions', 'label': 'Report', 'field': 'actions', 'align': 'center'},
                ], rows=[], row_key='id').classes('w-full')
                
                student_table.add_slot('body-cell-actions', '''
                    <q-td :props="props">
                        <q-btn icon="download" flat dense color="primary" @click="$parent.$emit('generate', props.row)"></q-btn>
                    </q-td>
                ''')
                student_table.on('generate', lambda msg: report.report(msg.args))
    load_table()

if __name__ in {"__main__", "__mp_main__"}:
    insert()
    
