from verifying_passcode import verify_user, add_user, reset_password
from nicegui import ui, app
import school_home_page
import teacher_page
from insert import insert
import sqlite3
from datetime import datetime

app_state = {
    'logged_in': False,
    'current_user': None
}

ui.colors(primary='#800000', secondary='#ffffff', accent='#f59e0b')

# Define your Admin credentials
ADMIN_ACCOUNTS = {
    "Apostle": "password1234",
    "Principal": "AdminPass2026",
    "Headmaster": "Secret123"
}

def update_login_activity(username, status='Active'):
    try:
        with sqlite3.connect('school_database.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS activity_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT, 
                    timestamp TEXT,
                    status TEXT
                )
            ''')
            if status == 'Active':
                cursor.execute("UPDATE activity_logs SET status = 'Inactive' WHERE status = 'Active'")
            current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
            cursor.execute('''
                INSERT INTO activity_logs (username, timestamp, status) 
                VALUES (?, ?, ?)
            ''', (username, current_timestamp, status))
            conn.commit()
    except Exception as e:
        print(f"Activity log error: {e}")

def login_page():
    with ui.column().classes('w-screen h-screen justify-center items-center bg-slate-50 m-0 p-0'):
        with ui.card().classes('w-[450px] p-8 bg-white shadow-2xl rounded-3xl border border-slate-100').tight():
            
            ui.label('Portal Access').classes('text-2xl font-bold text-[#800000] text-center w-full mb-6')

            with ui.tabs().classes('w-full bg-slate-50 rounded-xl p-1') as tabs:
                login_tab = ui.tab('login').classes('flex-1')
                register_tab = ui.tab('Register').classes('flex-1')
                reset_tab = ui.tab('Reset').classes('flex-1')
                
            with ui.tab_panels(tabs, value=login_tab).classes('w-full bg-transparent mt-4'):
                
                # --- LOGIN ---
                with ui.tab_panel(login_tab).classes('flex flex-col gap-4'):
                    username_input = ui.input('Username').classes('w-full').props('outlined dense')
                    password_input = ui.input('Password', password=True, password_toggle_button=True).classes('w-full').props('outlined dense')

                    def handle_page():
                        username = username_input.value.strip()
                        password = password_input.value
                        
                        if not username or not password:
                            ui.notify('Please fill the fields', type='warning', position='top')
                            return

                        if verify_user(username, password): 
                            app_state['logged_in'] = True 
                            app_state['current_user'] = username
                            update_login_activity(username, 'Active')
                            
                            # Role-based Routing
                            if username in ADMIN_ACCOUNTS and ADMIN_ACCOUNTS[username] == password:
                                ui.navigate.to('/home')
                            else:
                                ui.navigate.to('/teacher')
                        else:
                            ui.notify('Invalid username or password', type='negative', position='top')

                    ui.button('SIGN IN', on_click=handle_page).classes('w-full py-3 mt-4 text-white font-bold bg-[#800000] rounded-xl')

                # --- REGISTER ---
                with ui.tab_panel(register_tab).classes('flex flex-col gap-4'):
                    reg_user = ui.input('Create Username').classes('w-full').props('outlined dense')
                    reg_email = ui.input('Email Address').classes('w-full').props('outlined dense')
                    reg_pass = ui.input('Password', password=True, password_toggle_button=True).classes('w-full').props('outlined dense')
                    
                    def handle_registration():
                        if not reg_user.value or not reg_email.value or not reg_pass.value:
                            ui.notify('All fields are required!', type='warning', position='top')
                            return
                        try:
                            add_user(reg_user.value.strip(), reg_pass.value, reg_email.value.strip())
                            ui.notify('Registration Successful!', type='positive', position='top')
                            tabs.set_value(login_tab)
                        except:
                            ui.notify('Registration failed.', type='negative', position='top')

                    ui.button('REGISTER', on_click=handle_registration).classes('w-full py-3 mt-2 text-white font-bold bg-[#800000] rounded-xl')

                # --- RESET ---
                with ui.tab_panel(reset_tab).classes('flex flex-col gap-4'):
                    reset_user = ui.input('Username').classes('w-full').props('outlined dense')
                    reset_email = ui.input('Email Address').classes('w-full').props('outlined dense')
                    reset_pass = ui.input('New Password', password=True, password_toggle_button=True).classes('w-full').props('outlined dense')

                    def handle_reset():
                        try:
                            reset_password(reset_user.value.strip(), reset_email.value.strip(), reset_pass.value)
                            ui.notify('Password updated!', type='positive', position='top')
                            tabs.set_value(login_tab)
                        except:
                            ui.notify('Reset failed.', type='negative', position='top')

                    ui.button('RESET PASSWORD', on_click=handle_reset).classes('w-full py-3 mt-2 text-white font-bold bg-[#800000] rounded-xl')
                    ui.link('Back to Login', '#').on('click', lambda: tabs.set_value(login_tab)).classes('text-sm text-slate-400 hover:text-[#800000] text-center w-full mt-2')

pages = ui.sub_pages(routes={
    '/' : login_page,
    '/login' : login_page,
    '/home' : school_home_page.home,
    '/teacher': teacher_page.teacher,
    '/insert': insert,
})
# Force the router container to be full width
pages.classes('w-full') 
ui.run(torage_secret='YOUR_SECURE_RANDOM_STRING_HERE',
        port=port, 
        host='0.0.0.0',
        reload=False)

