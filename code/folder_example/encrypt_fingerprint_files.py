import os
import cv2
import numpy as np
from cryptography.fernet import Fernet
from encryption_module import encrypt_file

def process_files(directory_path, key):
    # Encrypt and decrypt files in the specified directory
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.tif'):
                input_file_path = os.path.join(root, file)
                output_file_path = os.path.join('fingerprint_dataset_encrypt', file)
                
                # Encrypt the file and save it with the .enc extension
                encrypt_file(input_file_path, key.encode())
                
                try:
                    # Rename the encrypted file to the output directory
                    os.rename(input_file_path + '.enc', output_file_path + '.enc')
                except Exception as e:
                    print(f"Error: {e}")
                    os.remove(input_file_path + '.enc')
def main():
    # Create a new directory to store the encrypted files
    os.makedirs('fingerprint_dataset_encrypt', exist_ok=True)

    # Generate a key for encryption
    #key = Fernet.generate_key()
    #print(f"key: {key}")

    key = "PqV8juaCaTmXcAXXMIF8qAcuzO2oPzDXKvBXQAkAo40="
    cipher_suite = Fernet(key)
                
    process_files('fingerprint_dataset', key)
    
if __name__ == "__main__":
    main()