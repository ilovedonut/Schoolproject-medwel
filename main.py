from function import *
import time
import os
import subprocess
import sys


def check_requirements():
    if not os.path.isfile("requirements.txt"):
        print("Error: requirements.txt not found. Exiting program.")
        sys.exit(1)

    with open("requirements.txt") as f:
        packages = f.read().splitlines()

    for package in packages:
        try:
            __import__(package.split('==')[0])
        except ImportError:
            print(f"{package} not found. Installing...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])

    print("All requirements are satisfied.")
    
check_requirements()

while True:
    print("\n|MEDWELL| - the future of health communication\n")
    print("1. Create an account")
    print("2. Login")
    print("3. connect custom database host")
    choice = input("Enter your choice: ")

    if choice == "1":
        create_account()
    elif choice == "2":
        user = login()
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
    elif choice == "3":
               host = input("Enter the database host (e.g., localhost): ")
               port = int(input("enter port for your host(e.g, 3306): "))
               user = input("Enter the database user: (eg, root) ")
               password = input("Enter the database password: (eg, admin)")
               database = input("Enter the database name (leave blank if not needed): ")
               connect_to_database(host,user,password,port,database)
    else:
         print("Invalid choice. Please try again.")
        
print("user found - ",)
print("loading data - .....")

if get_user_first_value(username) == 1:
    p = input("Doctor enter 2 , patient enter 1    -->  ")
    if p == "2":
        cursor.execute(
            "UPDATE users SET role = 'doctor' WHERE username = %s", (username,)
        )
        print("your account has succesfully been changed to doctors list")
        time.sleep(2)
        print("succesfully finished account initialization")
        update_user_first_value(username, "2")
    else:
        print("role changed to patient")
        update_user_first_value(username, "2")
        
time.sleep(0.5)
print("loading user complete")
notif = notif_grab(username)
time.sleep(0.5)
print("loading functionality")
time.sleep(0.5)
print("__________________________")
print("Welcome back to medwel")
time.sleep(0.6)

if notif >= 1:
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
        if menu == 1:
            display_messages_with_senders(get_user_id(username))
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

                save_doctor_id(doc78, get_user_id(username))
                print("connection succesful \n")
                print("YOUR PATIENTS INFO - ", get_doctor_info(doc78), "\n\n")

                time.sleep(3)
            elif po == "no":
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
        print("6 - add a new routine/prescription")
        menu = int(input("enter number - "))
        if menu == 1:
            display_messages_with_senders(get_user_id(username))
        if menu == 2:
            doc78 = input("enter you doctors medwel id - ")
            print("are you sure about your choice? enter yes or no \n ")
            po = input("")
            if po == "yes":
                print("connecting to doctor \n")
                time.sleep(1)

                save_doctor_id(get_user_id(username), doc78)
                print("connection succesful \n")
                print("YOUR DOCOTRS INFO - ", get_doctor_info(doc78), "\n\n")

                time.sleep(3)
            elif po == "no":
                print("ABORTING \n")
                continue
            else:
                print("\n enter a valid response \n")
                time.sleep(1)
                continue
        if menu == 3:
            email_new = input("enter new email")
        if menu == 4:
            input_area = input("enter pincode to search for doctors -")
            print("list of doctors - \n")
            print(doctor_list(input_area))
            varuseless = input(print(" \n \n TO GO BACK ENTER ANYTHING - "))
        
            new_email(email_new)
        if menu == 5:
            doctor_id = input("Enter your doctor's Medwel ID: ")
            message_text = input("Enter your message: ")
            sender_id = get_user_id(username)  # Get the sender's ID
            recipient_id = doctor_id  # Assuming the doctor ID is the recipient ID
            send_message(sender_id, recipient_id, message_text)
        if menu == 6:
            patient_id = get_user_id(username)
            add_routine(patient_id)