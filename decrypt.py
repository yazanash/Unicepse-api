from cryptography.fernet import Fernet
import os


def decrypt_file():
    key = os.getenv('ENCRYPTION_KEY').encode()
    cipher_suite = Fernet(key)

    with open('uni.json.enc', 'rb') as file:
        encrypted_data = file.read()

    decrypted_data = cipher_suite.decrypt(encrypted_data)

    with open(os.getenv('DECRYPT_FILE'), 'wb') as file:
        file.write(decrypted_data)
