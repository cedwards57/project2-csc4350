from cryptography.fernet import Fernet
import os
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

password_key = os.getenv("PASSWORD_KEY")


def encrypt_password(password):
    fernet = Fernet(password_key)
    encrypted_password = fernet.encrypt(password.encode())
    return encrypted_password


def decrypt_password(encrypted_password):
    fernet = Fernet(password_key)
    password = fernet.decrypt(encrypted_password).decode()
    return password


print(encrypt_password("pfsjdfs"))
