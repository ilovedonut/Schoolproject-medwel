import mysql.connector
import time
import csv
import os

CONFIG_FILE = 'database_config.csv'

def connect_to_database():
        global conn
        global cursor
        config = load_database_config()
        conn = mysql.connector.connect(
        host=config['host'],
        user=config['user'],
        password=config['password'],
        port=config['port'],
        database=config['database']
        )
        print("Connection to database successful!")
        cursor = conn.cursor()
        import init
        time.sleep(1)
        return conn
def save_database_config(host, user, password, port, database):
    
    with open(CONFIG_FILE, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['host', 'user', 'password', 'port', 'database'])
        writer.writerow([host, user, password, port, database])

def load_database_config():
    
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            reader = csv.reader(f)
            next(reader)  # Skip header row
            row = next(reader, None)
            if row:
                return {
                    'host': row[0],
                    'user': row[1],
                    'password': row[2],
                    'port': int(row[3]),
                    'database': row[4]
                }
    return None        


def save_doctor_id(user_id, doctor_id):
    query = "INSERT INTO medical (id, doctors) VALUES (%s, %s) ON DUPLICATE KEY UPDATE doctors = %s"
    cursor.execute(query, (user_id, doctor_id, doctor_id))
    conn.commit()


def send_message(sender_id, recipient_id, message_text):
    query = "INSERT INTO messages (sender_id, recipient_id, message_text) VALUES (%s, %s, %s)"
    cursor.execute(query, (sender_id, recipient_id, message_text))
    conn.commit()


def get_messages(user_id):
    query = "SELECT * FROM messages WHERE recipient_id = %s"
    cursor.execute(query, (user_id,))
    messages = cursor.fetchall()
    return messages


def get_user_role(username):
    user_id = get_user_id(username)
    query = "SELECT role FROM users WHERE id = %s"
    cursor.execute(query, (user_id,))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        return None


def notif_grab(username):
    try:
        user_id = get_user_id(username)
        cursor.execute("SELECT notifs FROM users WHERE id = %s", (user_id,))
        result = cursor.fetchone()
        return result[0] if result else 0
    except Exception as e:
        print(f"Error in notif_grab: {e}")
        return 0

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
    cursor.execute(
        """
        INSERT INTO users (username, password, email, area)
        VALUES (%s, %s, %s, %s)
    """,
        (username, password, email, area),
    )
    print(" succesful \n")
    conn.commit()


def login():
    global username
    username = input("Confirm your username: ")
    password = input("Enter your password: ")
    cursor.execute(
        """
        SELECT * FROM users
        WHERE username = %s AND password = %s
    """,
        (username, password),
    )
    user = cursor.fetchone()
    return username


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
    cursor.execute(query, (pin,))
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

def add_routine(patient_id):
    routine_description = input("Enter routine description: ")
    routine_type = input("Enter routine type (e.g., medication, exercise): ")
    start_date = input("Enter start date (YYYY-MM-DD): ")
    end_date = input("Enter end date (YYYY-MM-DD) or leave blank: ")

    # If end_date is not provided, set it to None
    if end_date == "":
        end_date = None

    # Insert the routine into the database
    cursor.execute(
        """
        INSERT INTO Routines (patient_id, routine_description, routine_type, start_date, end_date)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (patient_id, routine_description, routine_type, start_date, end_date)
    )
    conn.commit()  # Commit the changes to the database
    print("Routine added successfully!")    