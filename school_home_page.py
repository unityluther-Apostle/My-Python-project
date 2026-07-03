from nicegui import ui

# Unified System UI Color Token Mappings
ui.colors(primary='#800000', secondary='#ffffff', accent='#f59e0b')

def home():
    # 1. Target the native NiceGUI wrapper style engine and force center layout parameters
    ui.query('.q-page, .nicegui-content').style('max-width: none !important; width: 100% !important; padding: 0 !important;')
    ui.query('.nicegui-content').classes('w-full min-h-screen justify-center items-center flex bg-slate-50 p-4')
    
    # 2. Main content column structural block (FIXED: Pulled back to 4 spaces)
    with ui.column().classes('w-full max-w-[95vw] xl:max-w-[85vw] gap-4'):
        
        # --- CUSTOM HEADER CONTAINER CARD --- (FIXED: Adjusted relative spacing nesting levels)
        with ui.card().classes('w-full p-2 bg-white shadow-md rounded-xl border border-slate-200').tight():
            with ui.row().classes('w-full items-center justify-between px-4 py-1'):
                
                # Left Section: System Branding Title Element
                with ui.row().classes('items-center gap-2'):
                    ui.icon('school', color='#800000').classes('text-2xl')
                    ui.label('AIM Pre-School').classes('text-lg font-bold text-slate-800')
                
                # Right Section: Navigation Tab Elements
                with ui.tabs().props('active-color="primary" indicator-color="primary" text-color="grey-7"') as nav_tabs:
                    home_tab = ui.tab('Home Dashboard', icon='dashboard')
                    teachers_tab = ui.tab('Add Instructors', icon='person_add')
                    reports_tab = ui.tab('Academic Records', icon='assignment')
                    progress_tab = ui.tab('Progress', icon='trending_up')
                    logout_tab = ui.tab('Log Out', icon='logout')

        # --- MAIN VIEWING BODY CONTAINER PANELS ---
        with ui.tab_panels(nav_tabs, value=home_tab).classes('w-full text-xl bg-transparent'):
            
            # PANEL 1: HOME VIEW INTERFACE AREA (MISSION CONTROL HUB)
            with ui.tab_panel(home_tab).classes('p-0 gap-4 flex flex-col'):
                
                # Top Introduction Card
                with ui.card().classes('w-full p-6 bg-white shadow-lg rounded-2xl border border-slate-200'):
                    ui.label("Welcome!").classes('text-h2 font-bold').style('color: #800000 !important')
                    ui.label('lets explore together.').classes('text-slate-500 text-sm')

                # WIDGET BLOCK A: SCHOOL PERFORMANCE METRICS
                with ui.row().classes('w-full gap-4 items-stretch'):
                    with ui.card().classes('flex-1 p-4 bg-white shadow-md rounded-2xl border border-slate-200'):
                        with ui.row().classes('items-center gap-2'):
                            ui.icon('analytics', color='#800000').classes('text-xl')
                            ui.label('School GPA Average').classes('text-xs font-bold uppercase text-slate-400').style('color: #800000 !important')
                        ui.label('76.8%').classes('text-3xl font-extrabold text-slate-800 mt-2')
                        ui.label('+2.4% from last term').classes('text-xs font-medium text-emerald-600')

                    with ui.card().classes('flex-1 p-4 bg-white shadow-md rounded-2xl border border-slate-200'):
                        with ui.row().classes('items-center gap-2'):
                            ui.icon('people', color='#800000').classes('text-xl')
                            ui.label('Attendance Rate').classes('text-xs font-bold uppercase text-slate-400').style('color: #800000 !important')
                        ui.label('94.2%').classes('text-3xl font-extrabold text-slate-800 mt-2')
                        ui.label('Target: 95.0%').classes('text-xs font-medium text-amber-600')

                    with ui.card().classes('flex-1 p-4 bg-white shadow-md rounded-2xl border border-slate-200'):
                        with ui.row().classes('items-center gap-2'):
                            ui.icon('done_all', color='#800000').classes('text-xl')
                            ui.label('Grading Progress').classes('text-xs font-bold uppercase text-slate-400').style('color: #800000 !important')
                        ui.label('85%').classes('text-3xl font-extrabold text-slate-800 mt-2')
                        ui.linear_progress(value=0.85, color='primary').classes('w-full mt-2')

                # Split horizontal alignment workspace row
                with ui.row().classes('w-full gap-4 items-stretch'):
                    
                    # WIDGET BLOCK B: FINAL REPORT APPROVAL QUEUE (Left Column)
                    with ui.card().classes('flex-1 p-5 bg-white shadow-md rounded-2xl border border-slate-200'):
                        with ui.row().classes('items-center gap-2 mb-2'):
                            ui.icon('rate_review', color='#800000').classes('text-xl')
                            ui.label('Final Report Approval Queue').classes('text-base font-bold text-slate-800').style('color: #800000 !important')
                        ui.label('Review and digitally sign completed class sheets before email dispatch.').classes('text-xs text-slate-400 mb-4')
                        
                        with ui.row().classes('w-full items-center justify-between p-2 bg-slate-50 rounded-xl border border-slate-100 mb-2'):
                            with ui.column().classes('gap-0'):
                                ui.label('Senior 4A - Mathematics').classes('text-sm font-bold text-slate-700')
                                ui.label('Submitted by Tr. Mukasa • 34 Students').classes('text-xs text-slate-400')
                            ui.button('Approve & Release', color='#A7F3D0').props('dense flat').classes('text-xs font-bold')

                        with ui.row().classes('w-full items-center justify-between p-2 bg-slate-50 rounded-xl border border-slate-100'):
                            with ui.column().classes('gap-0'):
                                ui.label('Senior 3B - Chemistry').classes('text-sm font-bold text-slate-700')
                                ui.label('Submitted by Tr. Namubiru • 29 Students').classes('text-xs text-slate-400').style('color: #800000 !important')
                            ui.button('Approve & Release', color='#A7F3D0').props('dense flat').classes('text-xs font-bold')

                    # WIDGET BLOCK C: SYSTEM ACTIVITY LOGS (Right Column)
                    with ui.card().classes('flex-1 p-5 bg-white shadow-md rounded-2xl border border-slate-200'):
                        with ui.row().classes('items-center gap-2 mb-2'):
                            ui.icon('list_alt', color='#800000').classes('text-xl')
                            ui.label('System Activity Logs').classes('text-base font-bold text-slate-800').style('color: #800000 !important')
                        ui.label('Streaming timeline of administrative events and database logs.').classes('text-xs text-slate-400 mb-4')
                        
                        with ui.row().classes('items-start gap-2 mb-2'):
                            ui.label('10:42 AM').classes('text-xs font-mono font-bold text-slate-400 mt-0.5')
                            ui.label('Account "tr.joe" updated continuous evaluation score for Student ID 104').classes('text-xs text-slate-600')
                        
                        with ui.row().classes('items-start gap-2 mb-2'):
                            ui.label('09:15 AM').classes('text-xs font-mono font-bold text-slate-400 mt-0.5')
                            ui.label('System backup successfully pushed to passkey.db storage block').classes('text-xs text-slate-600')

                        with ui.row().classes('items-start gap-2'):
                            ui.label('08:00 AM').classes('text-xs font-mono font-bold text-slate-400 mt-0.5')
                            ui.label('Admin Account "apostle" updated system global color token schema parameters').classes('text-xs text-slate-600')

            # PANEL 2: TEACHERS ENTRY WORKSPACE
            with ui.tab_panel(teachers_tab).classes('p-0'):
                with ui.card().classes('w-full p-6 bg-white shadow-lg rounded-2xl border border-slate-200'):
                    ui.label('Instructor Registration desk').classes('text-h5 font-bold text-slate-800 mb-4')
                    ui.input(label='Instructor Name').classes('w-full max-w-md')
                    ui.button('Save Account', color='#800000').classes('mt-4 text-white')

            # PANEL 3: ACADEMIC EVALUATION REPORTS VIEW
            with ui.tab_panel(reports_tab).classes('p-0'):
                with ui.card().classes('w-full p-6 bg-white shadow-lg rounded-2xl border border-slate-200'):
                    ui.label('Academic Evaluation Reports Module').classes('text-h5 font-bold text-slate-800 mb-4')
