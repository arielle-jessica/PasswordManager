import os
import random
import string
import mysql.connector
from flask import Flask, request, jsonify, send_from_directory, make_response
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from duo_client import Auth
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes # type: ignore
from cryptography.hazmat.backends import default_backend # type: ignore
from cryptography.hazmat.primitives import padding # type: ignore

app = Flask(__name__, static_folder='public')
ph = PasswordHasher()


client = Auth(
    ikey='xxxxxxxxxxxxxx',
    skey='xxxxxxxxxxxxxxxxx',
    host='xxxxxxxxxxxxxxxxx'
)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="xxxxxxxxxxxxxx",
    database="xxxxxxxxxxxx"
)
cursor = db.cursor()

# Generating keys (for demonstration purposes)
KEY = os.urandom(32)  # 32 bytes for AES-256
IV = os.urandom(16)   # 16 bytes for AES

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


@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'popup.html')

@app.route('/authenticate-duo', methods=['POST'])
def authenticate_duo():
    data = request.get_json()
    username = data.get('username')
    passcode = data.get('passcode')

    try:
        response = client.auth(username=username, factor='passcode', passcode=passcode)

        if response.get('result') == 'allow':
            return jsonify({"success": True, "message": "Authentication successful Welcome!"})
        else:
            return jsonify({"success": False, "message": response.get('status_msg', 'Authentication denied.')})
    except Exception as e:
        return jsonify({"success": False, "message": f"Error: {e}"})

@app.route('/')
def home():
    return "Welcome to the Password Manager API!"

def get_master_password_hash():
    try:
        with open('xxxxxxxxxx', 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        return None

def save_master_password_hash(password_hash):
    with open('xxxxxxxxxxxxx.txt', 'w') as file:
        file.write(password_hash)

@app.route('/change-master-password', methods=['POST'])
def change_master_password():
    data = request.get_json()
    current_password = data.get('currentPassword')
    new_password = data.get('newPassword')

    if not current_password or not new_password:
        return jsonify({"success": False, "message": "Both current and new passwords are required."})

    try:
        # Fetch the stored hash of the current master password
        stored_hash = get_master_password_hash()

        if not stored_hash:
            return jsonify({"success": False, "message": "Current password not set or not found."})

        # Verify the current password
        ph = PasswordHasher()
        try:
            ph.verify(stored_hash, current_password)
        except VerifyMismatchError:
            return jsonify({"success": False, "message": "Current password is incorrect."})

        # Hash the new master password and store it
        new_password_hash = ph.hash(new_password)
        save_master_password_hash(new_password_hash)

        return jsonify({"success": True, "message": "Master password changed successfully."})

    except Exception as e:
        # Log the exception (you can use logging instead of print in production)
        print(f"Error: {e}")
        return jsonify({"success": False, "message": "An error occurred while changing the master password."})


@app.route('/retrieve-password', methods=['POST'])
def handle_retrieve_password():
    data = request.get_json()
    website = data.get('website')

    if not website:
        return jsonify({"success": False, "message": "Website name is required."})

    cursor.execute("SELECT password FROM passwords WHERE website = %s", (website,))
    result = cursor.fetchone()

    if result:
        encoded_password = result[0]
        try:
            decrypted_password = decrypt_password(encoded_password)
            return jsonify({"success": True, "password": decrypted_password})
        except Exception as e:
            return jsonify({"success": False, "message": f"Decryption error: {str(e)}"})
    else:
        return jsonify({"success": False, "message": "No password found for the given website."})

@app.route('/developer-info')
def serve_developer_info():
    return send_from_directory(app.static_folder, 'developer-info.html')


@app.route('/generate-password', methods=['GET', 'POST'])
def generate_password():
    if request.method == 'GET':
        return send_from_directory(app.static_folder, 'generate-password.html')
    
    if request.method == 'POST':
        data = request.get_json()
        length = data.get('length')
        website = data.get('website')
        username = data.get('username')
        email = data.get('email')
        desired_chars = data.get('desiredChars', '')

        if not (length and website and username and email):
            return jsonify({"success": False, "message": "All fields are required."})

        if not isinstance(length, int) or length <= 0:
            return jsonify({"success": False, "message": "Length must be a positive integer."})

        cursor.execute("SELECT password FROM passwords WHERE website = %s", (website,))
        existing_password = cursor.fetchone()
        
        if existing_password:
            return jsonify({"success": False, "message": "The website already has an existing password."})

        characters = string.ascii_letters + string.digits + string.punctuation
        desired_chars = ''.join(char for char in desired_chars if char in characters)

        remaining_length = length - len(desired_chars)
        if remaining_length < 0:
            return jsonify({"success": False, "message": "Desired characters exceed the specified length."})

        random_password = ''.join(random.choice(characters) for _ in range(remaining_length))
        password = desired_chars + random_password
        encrypted_password = encrypt_password(password)
        
        try:
            cursor.execute("INSERT INTO passwords (website, username, email, password) VALUES (%s, %s, %s, %s)", (website, username, email, encrypted_password))
            db.commit()
        except Exception as e:
            return jsonify({"success": False, "message": f"Database error: {e}"})
        
        return jsonify({"success": True, "message": "Password generated successfully."})


@app.route('/search', methods=['POST'])
def search():
    criteria = request.json['criteria']
    term = request.json['term']
    query = f"SELECT * FROM passwords WHERE {criteria} LIKE %s"
    cursor.execute(query, ('%' + term + '%',))
    results = cursor.fetchall()
    return jsonify(success=True, results=results)

@app.route('/delete-password', methods=['POST'])
def delete_password():
    cursor.execute("DELETE FROM passwords")
    db.commit()
    return jsonify(success=True, message='All passwords deleted successfully.')

def get_master_password_hash():
    cursor.execute("SELECT password_hash FROM master_password LIMIT 1")
    return cursor.fetchone()[0]

def save_master_password_hash(hash):
    cursor.execute("UPDATE master_password SET password_hash = %s WHERE id = 1", (hash,))
    db.commit()

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    if os.path.isfile(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return 'File not found', 404

if __name__ == '__main__':
    app.run(port=5000, debug=True)
