import mysql.connector
import time

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="admin",
    auth_plugin="mysql_native_password",
)
cursor = conn.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS user_ids")
cursor.execute("USE user_ids")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
                    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(50) NOT NULL,
                    role VARCHAR(20) NOT NULL DEFAULT 'patient',
                    password VARCHAR(255) NOT NULL,
                    first INT(20) DEFAULT 1,
                    email VARCHAR(100) NOT NULL,
                    notifs INT DEFAULT 1
         )
               
""")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS medical (
               id INT references users.id ,
               med_data varchar(100) ,
               doctors varchar(50) ,
               feedback varchar(50)
                     
         )
               
""")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id INT AUTO_INCREMENT,
        sender_id INT,
        recipient_id INT,
        message_text TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (id)
    )
""")  
def save_doctor_id(user_id, doctor_id):
    query = "INSERT INTO medical (id, doctors) VALUES (%s, %s) ON DUPLICATE KEY UPDATE doctors = %s"
    cursor.execute(query, (user_id, doctor_id, doctor_id))
    conn.commit()

def send_message(sender_id, recipient_id, message_text):
    query = "INSERT INTO messages (sender_id, recipient_id, message_text) VALUES (%s, %s, %s)"
    cursor.execute(query, (sender_id, recipient_id, message_text))
    cnx.commit()

def get_messages(user_id):
    query = "SELECT * FROM messages WHERE recipient_id = %s"
    cursor.execute(query, (user_id,))
    messages = cursor.fetchall()
    return messages
    
def get_user_role(username):
    query = "SELECT role FROM users WHERE username = %s"
    cursor.execute(query, (username,))
    result = cursor.fetchone()
    if result:
        return result[0]  
    else:
        return None
def notif_grab(username):
    query = "SELECT notifs FROM users WHERE username = %s"
    cursor.execute(query, (username,))
    result = cursor.fetchone()
    if result:
        
        return result[0]  
    else:
        return None
    
def update_user_first_value(username, new_value):

    query = "UPDATE users SET first = %s WHERE username = %s"
    cursor.execute(query, (new_value, username))

    conn.commit()
    print(f"Updated first value for user {username} to {new_value}")
    
def get_user_first_value(username):
    query = "SELECT first FROM users WHERE username = %s"
    cursor.execute(query, (username,))
    result = cursor.fetchone()
    if result:
        
        return result[0]  # Return the value of the "1st" column
    else:
        return None 

def create_account():
    username = input("Enter a username: ")
    password = input("Enter a password: ")
    email = input("Enter an email: ")
    time.sleep(1)
    print("\n registering user \n")
    time.sleep(2)
    cursor.execute("""
        INSERT INTO users (username, password, email)
        VALUES (%s, %s, %s)
    """, (username, password, email))
    print(" succesful \n")
    conn.commit()

def login():
    global username
    username = input("Enter your username: ")
    password = input("Enter your password: ")  
    global user
    cursor.execute("""
        SELECT * FROM users
        WHERE username = %s AND password = %s
    """, (username, password))
    user = cursor.fetchone()

def delete_account(username):
    query = "DELETE FROM users WHERE username = %s"
    cursor.execute(query, (username,))

    conn.commit()
    print(f"Account for {username} deleted successfully!")

def get_user_id(username):
    cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
    result = cursor.fetchone()
    if result:
        return result[0]  
def get_doctor_info(doctor_id):
    query = "SELECT username,role,email FROM users WHERE id = %s AND role = 'doctor'"
    cursor.execute(query, (doctor_id,))
    doctor_info = cursor.fetchone()
    return doctor_info

while True:
    print("1. Create an account")
    print("2. Login")
    choice = input("Enter your choice: ")

    if choice == "1":
        create_account()
    elif choice == "2":
        login()
        if user == None:
            print("Invalid username or password")
            time.sleep(2)
            print("\n\nwait 5 seconds to return to sign up screen")
            time.sleep(3)
            continue
        else:
            break
    elif choice == "2007special":
        deluser = input("enter username to delete - ")
        delete_account(deluser)
    else:
        print("Invalid choice. Please try again.")
print("user found - ",user)
print("loading data - .....")

if get_user_first_value(username) == 1 :
  p = input("Doctor enter 2 , patient enter 1    -->  ")
  if p == "2" :
      cursor.execute("UPDATE users SET role = 'doctor' WHERE username = %s", (username,))
      print("your account has succesfully been changed to doctors list")
      time.sleep(2)
      print("succesfully finished account initialization")
      update_user_first_value(username,"2")
  else:
      print("role changed to patient")
      update_user_first_value(username,"2")         
time.sleep(2)
print("loading user complete")
notif = notif_grab(username)
time.sleep(2)
print("loading functionality")
time.sleep(2)
print("__________________________")
print("Welcome back to medwel")
time.sleep(2)
if notif >= 1 :
    print(f"\n \n  You have {notif-1} new notifications \n \n ")
if get_user_role(username) == "patient":
 while True:

  print("     Main Menu     ")
  print("enter number according to desired selection")
  print("1 - read notification")
  print("2 - connect with a doctor")
  print("3 - customize user id")
  print("4 - get a list of doctors")
  print("5 - send feedback to a connected doctor")
  print("6 - enter your current medicne routine/ prescription")
  menu = input("enter number - ")
  if menu == 2:
   doc78 = input("enter you doctors medwel id - ")
   print("are you sure about your choice? enter yes or no \n ")
   po = input("")
   if po == "yes":
      print("connecting to doctor \n")
      time.sleep(1)
      
      save_doctor_id(get_user_id(username), doc78)
      print("connection succesful \n")
      print("YOUR DOCOTRS INFO - ",get_doctor_info(doc78),"\n\n")

      time.sleep(3)
   elif po == "no" :
       print("ABORTING \n")
       continue
   else:
      print("\n enter a valid response \n")
      time.sleep(1)
      continue