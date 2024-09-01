from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes # type: ignore
from cryptography.hazmat.backends import default_backend # type: ignore
from cryptography.hazmat.primitives import padding # type: ignore
import os

KEY = os.urandom(32)  # Generate a 32-byte key (256-bit)
IV = os.urandom(16)   # Generate a 16-byte IV (128-bit)

def encrypt_password(password):
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_password = padder.update(password.encode()) + padder.finalize()

    cipher = Cipher(algorithms.AES(KEY), modes.CBC(IV), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_password = encryptor.update(padded_password) + encryptor.finalize()
    return encrypted_password

def decrypt_password(encrypted_password):
    cipher = Cipher(algorithms.AES(KEY), modes.CBC(IV), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_password = decryptor.update(encrypted_password) + decryptor.finalize()

    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    unpadded_password = unpadder.update(decrypted_password) + unpadder.finalize()
    return unpadded_password.decode()

# Encrypt a known password
encrypted = encrypt_password('mypassword')
print("KEY:", KEY)
print("IV:", IV)
print("Encrypted Password:", encrypted)

# Decrypt it back
decrypted = decrypt_password(encrypted)
print("Decrypted:", decrypted)