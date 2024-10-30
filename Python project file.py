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
                    area VARCHAR(20) NOT NULL,
                    email VARCHAR(100) ,
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
def check_username_exists(username):
    query = "SELECT COUNT(*) FROM users WHERE username = %s"
    cursor.execute(query, (username,))
    count = cursor.fetchone()[0]
    return count > 0
def check_email_exists(email):
    query = "SELECT COUNT(*) FROM users WHERE email = %s"
    cursor.execute(query, (email,))
    count = cursor.fetchone()[0]
    return count > 0
def create_account():
    username = input("Enter a username: ")
    if check_username_exists(username):
        print("Username already exists. Please choose a different username.")
        time.sleep(1)
        print("\n \n")
        time.sleep(1)
        return
    password = input("Enter a password: ")
    email = input("Enter an email: ")
    if check_email_exists(email):
        print("Email already exists. Please choose a different email.")
        time.sleep(1)
        print("\n \n")
        time.sleep(1)
        return
    area = input("enter your pincode")
    time.sleep(1)
    print("\n registering user \n")
    time.sleep(2)
    cursor.execute("""
        INSERT INTO users (username, password, email, area)
        VALUES (%s, %s, %s, %s)
    """, (username, password, email, area))
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
def doctor_list(pin):
     query = "SELECT username,role,email,area FROM users WHERE area = %s AND role = 'doctor' "
     cursor.execute(query,(pin,))
     doctor_info = cursor.fetchall()
     return doctor_info 
def new_email(new):
    print("feature still in development ")
def display_messages_with_senders(user_id):
    query = """
    SELECT m.message_text, m.created_at, u.username 
    FROM messages m 
    JOIN users u ON m.sender_id = u.id 
    WHERE m.recipient_id = %s
    ORDER BY m.created_at DESC
    """
    cursor.execute(query, (user_id,))
    messages = cursor.fetchall()
    
    if not messages:
        print("\nNo messages found.\n")
        time.sleep(2)
        return

    for message in messages:
        message_text, created_at, sender_username = message
        print(f"[{created_at}] {sender_username}: {message_text}")
def send_message(sender_id, recipient_id, message_text):
    query = "INSERT INTO messages (sender_id, recipient_id, message_text) VALUES (%s, %s, %s)"
    cursor.execute(query, (sender_id, recipient_id, message_text))
    conn.commit()
    print("Message sent successfully!")        
while True:
    print("\n|MEDWELL| - the future of health communication\n")
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
time.sleep(0.5)
print("loading user complete")
notif = notif_grab(username)
time.sleep(0.5)
print("loading functionality")
time.sleep(0.5)
print("__________________________")
print("Welcome back to medwel")
time.sleep(0.6)
if notif >= 1 :
    print(f"\n \n  You have {notif-1} new notifications \n \n ")
if get_user_role(username) == "doctor":
 while True:
  print("__________________________")
  print("     Main Menu     ")
  print("enter number according to desired selection")
  print("1 - read notification")
  print("2 - enter patient medwel id")
  print("3 - change email")
  print("4 - get a list of doctors")
  print("5 - send feedback to a connected patient")
  menu = int(input("enter number - "))
  if menu == 5:       
       doctor_id = input("Enter your patient's Medwel ID: ")
       message_text = input("Enter your message: ")
       sender_id = get_user_id(username)  # Get the sender's ID
       recipient_id = doctor_id  # Assuming the doctor ID is the recipient ID
       send_message(sender_id, recipient_id, message_text)
  if menu == 2:
   doc78 = input("enter you patients medwel id - ")
   print("are you sure about your choice? enter yes or no \n ")
   po = input("")
   if po == "yes":
      print("connecting to doctor \n")
      time.sleep(1)
      
      save_doctor_id(doc78 , get_user_id(username))
      print("connection succesful \n")
      print("YOUR PATIENTS INFO - ",get_doctor_info(doc78),"\n\n")

      time.sleep(3)
   elif po == "no" :
       print("ABORTING \n")
       continue
   else:
      print("\n enter a valid response \n")
      time.sleep(1)
      continue
  elif menu == 4:
      input_area = input("enter pincode to search for doctors - ")
      print("list of doctors - \n")
      print(doctor_list(input_area))
      varuseless = input(print(" \n \n TO GO BACK ENTER ANYTHING - "))
  elif menu == 3:
      email_new = input("enter new email - ")  
      new_email(email_new)  
if get_user_role(username) == "patient":
 while True:
  print("__________________________")
  print("     Main Menu     ")
  print("enter number according to desired selection")
  print("1 - read notification")
  print("2 - connect with a doctor")
  print("3 - customize email id")
  print("4 - get a list of doctors")
  print("5 - send feedback/message to a connected doctor")
  print("6 - enter your current medicne routine/ prescription")
  menu = int(input("enter number - "))
  if menu == 1:
      display_messages_with_senders(get_user_id(username))
  if menu == 5:       
       doctor_id = input("Enter your doctor's Medwel ID: ")
       message_text = input("Enter your message: ")
       sender_id = get_user_id(username)  # Get the sender's ID
       recipient_id = doctor_id  # Assuming the doctor ID is the recipient ID
       send_message(sender_id, recipient_id, message_text)
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
  elif menu == 4:
      input_area = input("enter pincode to search for doctors -")
      print("list of doctors - \n")
      print(doctor_list(input_area))
      varuseless = input(print(" \n \n TO GO BACK ENTER ANYTHING - "))
  elif menu == 3:
      email_new = input("enter new email")  
      new_email(email_new)