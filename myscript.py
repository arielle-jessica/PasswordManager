
import duo_client
from duo_client import Auth
import os
import string
import random
import getpass
import argon2
import time
import sys
import mysql.connector
from argon2.exceptions import VerifyMismatchError
from prettytable import PrettyTable
import pyperclip
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes # type: ignore
from cryptography.hazmat.backends import default_backend  # type: ignore
from cryptography.hazmat.primitives import padding # type: ignore

client = Auth(
    ikey='xxxxxxxxxxxxxxxxxxxxx',
    skey='xxxxxxxxxxxxxxxxxxxxxxxxx',
    host='xxxxxxxxxxxxxxxxxxxxxxxxxxx'
)

KEY = os.urandom(32) 
IV = os.urandom(16)


def authenticate_duo():
    username = input("Please enter your name: ")
    passcode = input("Please input your Duo Mobile passcode: ")

    try:
        response = client.auth(username=username, factor='passcode', passcode=passcode)

        if response.get('result') == 'allow':
            print("Authentication successful!")
            return True
        else:
            print("Authentication denied.")
            print(f"Reason: {response.get('status_msg', 'Unknown reason')}")
            return False
    except Exception as e:
        print(f"Error: {e}")
        return False

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="xxxxxxxxxxxxxxxxxx",
    database="xxxxxxxxxxxxxxxxxxxxxxx"
)
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS passwords
                  (website VARCHAR(255), username VARCHAR(255),
                  email VARCHAR(255), password BLOB)''')

master_password_hash = None

TIMEOUT_SECONDS = 60

last_interaction_time = time.time()

def check_activity():
    global last_interaction_time
    last_interaction_time = time.time()

def is_timeout():
    current_time = time.time()
    elapsed_time = current_time - last_interaction_time
    return elapsed_time > TIMEOUT_SECONDS

def show_front_page():
    ascii_art = (
        "||||||||   |||||||||              |||             ||||||||||||||||||\n"
        "||||||||   ||       ||          ||   ||           ||||||||||||||||||\n"
        "   ||      ||       ||       ||       ||                    |||\n"
        "   ||      ||       ||       ||         ||                  |||\n"
        "   ||      ||||||||||       ||           ||                 |||\n"
        "   ||      ||        ||    |||||||||||||||||                |||\n"
        "   ||      ||         ||  ||               ||               |||\n"
        "   ||      ||         || ||                 ||              |||\n"
        "   ||      ||        || ||                   ||             |||\n"
        "||||||||   ||       || ||                     ||            |||\n"
        "||||||||   |||||||||  ||                       ||  ||||||||||||\n"
    )

    print(ascii_art)

    print("Welcome to Your Password Manager\n")
    entered_password = getpass.getpass("Please enter your master password: \n")

    if validate_master_password(entered_password) and authenticate_duo():
        print("Authentication successful. Welcome!\n")
        while True:
            check_activity()
            main_menu()

            if is_timeout():
                print("Timeout: No activity detected. Logging out...")
                break
            time.sleep(60)

        print("Timeout. Exiting...\n")
        choice = input("Would you like to log in again? (Yes/No): \n").lower()
        if choice == "yes":
            show_front_page()
        elif choice == "no":
            print("Exiting... Bye\n")
        else:
            print("Invalid choice. Exiting... Bye\n")
    else:
        print("Authentication failed. Access denied.")
        authenticate_user()

def validate_master_password(password):
    global master_password_hash
    hasher = argon2.PasswordHasher()
    try:
        return hasher.verify(master_password_hash, password)
    except VerifyMismatchError:
        return False

def authenticate_user():
    global master_password_hash
    print("Authentication required for Password Reset.\n")
    question1 = input("What is your favourite color? \n")
    question2 = input("In which city were you born? \n")

    if question1.lower() == "xxxxxxxxx" and question2.lower() == "xxxxxxxxxxxxxx":
        reset_password()
        main_menu()
    else:
        print("Authentication failed. Exiting... Bye\n")

def save_master_password_hash(password_hash):
    with open('xxxxxxxxxxx.txt', 'w') as f:
        f.write(password_hash)

def reset_password():
    global master_password_hash
    new_password = getpass.getpass("Enter a new master password: \n")
    hasher = argon2.PasswordHasher()
    master_password_hash = hasher.hash(new_password)
    with open('xxxxxxxxxxxxxxxxx.txt', 'w') as f:
        f.write(master_password_hash)
    print("Password reset successful. You can now log in with your new password.\n")

def main_menu():
    while True:
        print("\n      Main Menu")
        print("1. Change Password")
        print("2. Retrieve Password")
        print("3. Generate Password")
        print("4. Search")
        print("5. Password Delete")
        print("6. Developer info")
        print("7. Exit")

        choice = input("Enter your choice (1-7): ")
        if choice == "1":
            change_password()
        elif choice == "2":
            retrieve_password()
        elif choice == "3":
            generate_password()
        elif choice == "4":
            search()
        elif choice == "5":
            password_delete()
        elif choice == "6":
            developer_info()
        elif choice == "7":
            print("Exiting... Bye")
            break
        else:
            print("Please select a number between 1 and 7.")

def change_password():
    entered_password = getpass.getpass("Enter your current password: ")
    if validate_master_password(entered_password):
        new_password = getpass.getpass("Enter a new master password: ")
        confirm_new_password = getpass.getpass("Confirm your new master password: ")

        if new_password == confirm_new_password:
            hasher = argon2.PasswordHasher()
            new_password_hash = hasher.hash(new_password)
            save_master_password_hash(new_password_hash)
            print("Password changed successfully.")
        else:
            print("Passwords do not match. Password change failed.")
    else:
        print("Invalid current password. Password change failed.")

def encrypt_password(password):
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_password = padder.update(password.encode()) + padder.finalize()

    cipher = Cipher(algorithms.AES(KEY), modes.CBC(IV), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_password = encryptor.update(padded_password) + encryptor.finalize()
    
    print(f"Encrypted password length: {len(encrypted_password)}")
    return encrypted_password

def decrypt_password(encrypted_password):
    cipher = Cipher(algorithms.AES(KEY), modes.CBC(IV), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_padded_password = decryptor.update(encrypted_password) + decryptor.finalize()

    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    decrypted_password = unpadder.update(decrypted_padded_password) + unpadder.finalize()
    
    print(f"Decrypted password length: {len(decrypted_password)}")
    return decrypted_password.decode()


def store_encrypted_password(website_name, username, email, password):
    encrypted_password = encrypt_password(password)
    
    cursor.execute("INSERT INTO passwords (website, username, email, password) VALUES (%s, %s, %s, %s)", 
                   (website_name, username, email, encrypted_password))
   
def retrieve_password():
    website_name = input("Enter the name of the website to retrieve the password: ")
    
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM passwords WHERE website = %s", (website_name,))
        result = cursor.fetchone()
        
        if result:
            password = result[0]
            if password:
                print(f"Password for {website_name}: {password}")
            else:
                print("No password found for this website.")
        else:
            print(f"Sorry, no password found for {website_name}.")
    
    except Exception as e:
        print(f"An error occurred: {e}")




def generate_password():
    length = int(input("Enter the desired length of the password: "))
    website = input("Enter the name of the website: ")
    username = input("Enter the desired username: ")
    email = input("Enter the email address: ")
    desired_password = input("Enter any desired characters for the password (optional): ")

    cursor.execute("SELECT password FROM passwords WHERE website = %s", (website,))
    existing_password = cursor.fetchone()

    if existing_password:
        choice = input("The website already has an existing password. Would you like to view the password? (Yes/No): ").lower()
        if choice == "yes":
            decrypted_password = decrypt_password(existing_password[0])
            print(f"The password for {website} is: {decrypted_password}")
        return

    characters = string.ascii_letters + string.digits + string.punctuation
    remaining_length = length - len(desired_password)
    random_password = ''.join(random.choice(characters) for _ in range(remaining_length))

    password = desired_password + random_password

    encrypted_password = encrypt_password(password)

    cursor.execute("INSERT INTO passwords (website, username, email, password) VALUES (%s, %s, %s, %s)",
                   (website, username, email, encrypted_password))
    conn.commit()

    print(f"Generated password for {website} is stored and encrypted in the database.")


def developer_info():
    print("     _____                       _             ")
    print("    |  __ \                     (_)            ")
    print("    | |  | | ___  _ __ ___   __ _ _ _ __   ___ ")
    print("    | |  | |/ _ \| '_ ` _ \ / _` | | '_ \ / _ \ ")
    print("    | |__| | (_) | | | | | | (_| | | | | |  __/")
    print("    |_____/ \___/|_| |_| |_|\__,_|_|_| |_|\___|")
    print("")
    print("#### Developer Info ####")
    print("Name:xxxxxxxxxxxxxxxxxxxxx")
    print("Email: xxxxxxxxxxxxxxx")
    print("LinkedIn: xxxxxxxxxxxxxxxxxxxxx")

def search():
    search_criteria = input("Enter search criteria (website, username, or email): ").lower()
    search_term = input("Enter search term: ")

    if search_criteria == "website":
        cursor.execute("SELECT * FROM passwords WHERE website LIKE %s", ('%' + search_term + '%',))
    elif search_criteria == "username":
        cursor.execute("SELECT * FROM passwords WHERE username LIKE %s", ('%' + search_term + '%',))
    elif search_criteria == "email":
        cursor.execute("SELECT * FROM passwords WHERE email LIKE %s", ('%' + search_term + '%',))
    else:
        print("Invalid search criteria. Please enter 'website', 'username', or 'email'.")
        return

    results = cursor.fetchall()

    if results:
        table = PrettyTable()
        table.field_names = ["Website", "Username", "Email", "Password"]
        for row in results:
            table.add_row(row)
        print(table)

        password_to_copy = decrypt_password(results[0][3])
        pyperclip.copy(password_to_copy)

        print("Password copied to clipboard!")

    else:
        print("No matching records found.")

def password_delete():
    global master_password_hash
    confirm = input("Are you sure you want to delete your master password? This action cannot be undone. (Yes/No): ").lower()
    if confirm == "yes":
        try:
            os.remove("master_password_hash.txt")
            print("Master password deleted successfully.")
            master_password_hash = None
        except FileNotFoundError:
            print("Master password file not found.")
    elif confirm == "no":
        print("Password deletion cancelled.")
    else:
        print("Invalid choice. Password deletion cancelled.")

def load_master_password_hash():
    global master_password_hash
    if os.path.exists('master_password_hash.txt'):
        with open('master_password_hash.txt', 'r') as f:
            master_password_hash = f.read()
    else:
        reset_password()

if __name__ == "__main__":
    load_master_password_hash()
    show_front_page()

conn.close()


