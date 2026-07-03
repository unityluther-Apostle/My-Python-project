from verifying_passcode import verify_user, add_user,reset_password
from nicegui import ui, app
import school_home_page
import teachers_page

# App state configuration nset
app_state = {
	'logged_in' : False,
	'current_user': None
}


# this block of code is for setting the primary, secondary colors
ui.colors(primary='#800000', secondary='#ffffff', accent='#f59e0b')

#ui.image('https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ4ttx_TwrbNdHnEBEyt-9c8c2yC0WZ8Ey9UqEBPrpvpg&s=10').classes('w-[200px] h-[200px] object-cover rounded-2xl').tight()


def login_page():
	
	with ui.column().classes('w-screen h-screen justify-center items-center bg-transparent m-0 p-0'):
		# this is a Single  card shared by  both login and registration tabs
		with ui.card().classes('w-[50vw] max-w-[500px] min-h-[500px] p-6 bg-white shadow-2xl rounded-2xl border-2 border-[#800000]').tight():


			# this is a  Navigation Header
			with ui.tabs().classes('w-full') as tabs:
				login_tab = ui.tab('login')
				register_tab = ui.tab('Register')
				reset_tab = ui.tab('Reset') #.classes('hidden')
				

			# this block of code is for the  Main Tab Body Container
			with ui.tab_panels(tabs, value=login_tab).classes('w-full bg-transparent'):
				
				# this is the tab for login 
				with ui.tab_panel(login_tab).classes('flex flex-col gap-4 items-center justify-center p-4'):
					ui.label('Please, Enter your details').classes('text-h5 font-bold text-slate-800 text-center')
					username_input = ui.input('Enter username').classes('w-full rounded-xl')
					password_input = ui.input('Enter password', password=True, password_toggle_button=True).classes('w-full rounded-xl')

					def handle_page():
						username = username_input.value.strip()
						password = password_input.value

					#this is the block of code for checking if all the fields are fully filled
						if not username or not password:
							ui.notify('Please fill the fields', type='warning', position='top')
							return
					#this block of code verifies the username and password with the database and acts as a temporay memory to keep the logged in session

						if verify_user(username, password): 
							app_state['logged_in'] = True 
							app_state['current_user'] = username

							ui.notify('Login successful', type='positive', position='top')
							ui.navigate.to('/teachers')
						else:
							ui.notify('invalid username or password', type='negative', position='top')

					ui.button('log-in', color='#800000', on_click=handle_page).classes('w-full rounded-xl py-3 text-white font-bold mt-4')

				# this block of code diplays the fields that one can fill in  create a user acc. and password
				with ui.tab_panel(register_tab).classes('flex flex-col gap-4 items-center justify-center p-4'):
					ui.label('Create an Account').classes('text-h5 font-bold text-slate-800 text-center')
					
					reg_user = ui.input('Create Username').classes('w-full rounded-xl')
					reg_email = ui.input('Enter Email Address').classes('w-full rounded-xl')
					reg_pass = ui.input('Create Password', password=True, password_toggle_button=True).classes('w-full rounded-xl')
					
					def handle_registration():
						username = reg_user.value.strip()
						email = reg_email.value.strip()
						password = reg_pass.value

						if not username or not email or not password:
							ui.notify('All fields are required!', type='warning', position='top')
							return

						try:
							add_user(username, password, email)
							ui.notify('Registration Successful! Please log in.', type='positive', position='top')

							# Reset fields on success
							reg_user.set_value('')
							reg_email.set_value('')
							reg_pass.set_value('')

							# this block of code allows one to go back to the login tab after one successfully creates a username and password
							tabs.set_value('login')
						except Exception as e:
							ui.notify('Registration failed. Username or email might be taken.', type='negative', position='top')

					ui.button('Register', color='#800000', on_click=handle_registration).classes('w-full rounded-xl py-3 text-white font-bold mt-2')


				#this block of code helps the user create a new password when he/she forgets it
				with ui.tab_panel(reset_tab).classes('flex flex-col gap-4 items-center justify-center p-4'):
					ui.label('Reset Your Password').classes('text-h5 font-bold text-slate-800 text-center')
					
					reset_user = ui.input('Confirm Username').classes('w-full rounded-xl')
					reset_email = ui.input('Confirm Email Address').classes('w-full rounded-xl')
					reset_pass = ui.input('Enter New Password', password=True, password_toggle_button=True).classes('w-full rounded-xl')

					def handle_reset():
						username = reset_user.value.strip()
						email = reset_email.value.strip()
						password = reset_pass.value

						if not username or not email or not password:
							ui.notify('All fields are required to verify identity!', type='warning', position='top')
							return

						try:
							reset_password(username, email, password)
							ui.notify('Password updated successfully! Please log in.', type='positive', position='top')
							
							#this block of code redirects the person to the login tab after resetting the password
							reset_user.set_value('')
							reset_email.set_value('')
							reset_pass.set_value('')
							tabs.set_value('login')
						except Exception as e:
							ui.notify('Reset failed! Account details do not match.', type='negative', position='top')

					ui.button('Update Password', color='#800000', on_click=handle_reset).classes('w-full rounded-xl py-3 text-white font-bold mt-2')
					ui.link('Back to Login').on('click', lambda: tabs.set_value('login')).classes('text-sm text-slate-500 hover:text-[#800000]')


#this is the block of code for setting the background

###ui.query('body').classes('bg-[linear-gradient(to_right,#FFFFFF_50%,#800000_50%)] m-0 p-0')

'''
with ui.element('div').classes('absolute inset-0 z-[-1] overflow-hidden'):
    ui.image('1.jpg').classes('w-full h-full object-cover')
'''
# thses are the Sub pages that are tracking routing layout
ui.sub_pages(routes={
	'/' : login_page,
	'/login' : login_page,
	'/home' : school_home_page.home,
    '/teachers' : teachers_page.teachers,
})

#ui.run(title=('School database system'))
# Force NiceGUI to run on Hugging Face's required port (7860) and host (0.0.0.0)

ui.run(
    title='School database system')
