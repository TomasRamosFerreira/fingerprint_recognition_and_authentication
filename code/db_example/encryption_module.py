import os
import cv2
import numpy as np
from cryptography.fernet import Fernet, InvalidToken

def encrypt_file(file_path, key):
    # Read the contents of the file
    with open(file_path, 'rb') as file:
        file_data = file.read()
    
    # Create a Fernet cipher suite using the provided key
    cipher_suite = Fernet(key)
    
    # Encrypt the file data
    encrypted_data = cipher_suite.encrypt(file_data)
    
    # Write the encrypted data to a new file with the .enc extension
    #with open(file_path + '.enc', 'wb') as file:
    #    file.write(encrypted_data)
        
    return encrypted_data

def decrypt_file(file_path, key):
    try:
        # Read the encrypted data from the file
        with open(file_path, 'rb') as file:
            encrypted_data = file.read()

        # Create a Fernet cipher suite using the provided key
        cipher_suite = Fernet(key)

        # Decrypt the data
        decrypted_data = cipher_suite.decrypt(encrypted_data)

        # Return the decrypted data
        return decrypted_data
    except InvalidToken:
        #print("Error: Invalid key. Decryption failed.")
        return None