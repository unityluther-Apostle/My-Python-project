import sqlite3
import bcrypt
import secrets
import string


passkey = "passkey.db"

Table = {
    "Users": '''Username TEXT UNIQUE, Password  BLOB, Email TEXT UNIQUE '''
 
 }

conn = sqlite3.connect("passkey.db")
cursor = conn.cursor()
cursor.execute("PRAGMA foreign_keys = ON;")

for table_name, columns in Table.items():
    query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns});"
    cursor.execute(query)
conn.commit()



try:
	cursor.execute("ALTER TABLE Users ADD COLUMN role TEXT ")
	conn.commit()
	print("success: 'role' column addes completely")

except sqlite3.OperationalError as e:
	print(f"Notice: {e}. the column likely exixts")

finally:
	conn.close()

conn.close()



#the database for students marks 
students = "students.db"

#the table for entering students marks 

conn = sqlite3.connect('students.db')
cursor = conn.cursor()

# Your complete, error-free academic schema block
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Students (
        student_ID INTEGER PRIMARY KEY AUTOINCREMENT, 
        student_name TEXT NOT NULL, 
        parent_email TEXT, 
        Class TEXT, 
        Class_Level TEXT, 
        quizzess REAL DEFAULT 0.0, 
        midterm_exam REAL DEFAULT 0.0, 
        end_of_term REAL DEFAULT 0.0, 
        teachers_remarks TEXT
    )
''')

conn.commit()
conn.close()
print("Students database schema successfully compiled!")





def generate_unique_username(first_name, last_name):
    """Generates a clean, unique username format: f.lastname"""
    base_username = f"{first_name[0].lower()}.{last_name.lower()}".replace(" ", "")
    username = base_username
    
    conn = sqlite3.connect(passkey)
    cursor = conn.cursor()
    
    # Safety Check Loop: If username exists, append an incrementing number
    counter = 1
    while True:
        cursor.execute("SELECT 1 FROM Users WHERE Username = ?", (username,))
        if not cursor.fetchone():
            break  # Username is completely unique, exit loop
        username = f"{base_username}{counter}"
        counter += 1
        
    conn.close()
    return username

def generate_secure_password(length=10):
    """Generates a secure, random alphanumeric password"""
    # Combines letters and numbers (excluding confusing characters like l, O, 1, 0)
    characters = string.ascii_letters + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))

def register_staff_member(first_name, last_name, email, role):
    """Automatically creates credentials and saves the user to passkey.db"""
    # 1. Run the automatic generation engines
    generated_username = generate_unique_username(first_name, last_name)
    generated_password = generate_secure_password()
    
    # 2. Insert into the SQLite Users table
    conn = sqlite3.connect(passkey)
    cursor = conn.cursor()
    
    try:
        # Note: We pass the password directly as text here to match your schema logic. 
        # (In production, you would convert the generated string to a hashed BLOB)
        cursor.execute('''
            INSERT INTO Users (Username, Password, Email, role) 
            VALUES (?, ?, ?, ?)
        ''', (generated_username, generated_password.encode('utf-8'), email, role))
        
        conn.commit()
        
        # 3. Return the generated credentials so you can display or email them
        return {
            "status": "success",
            "username": generated_username,
            "password": generated_password
        }
        
    except sqlite3.IntegrityError:
        return {"status": "error", "message": "Email address is already registered."}
    finally:
        conn.close()

# --- Example Usage ---
# When the admin adds a new teacher:
new_account = register_staff_member("Sarah", "Namubiru", "sarah.n@school.edu", "teacher")
print(new_account)


