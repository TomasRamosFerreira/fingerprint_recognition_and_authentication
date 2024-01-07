import os
import cv2
import numpy as np
from cryptography.fernet import Fernet
from encryption_module import encrypt_file
from database_manager_module import connect_database, close_database_connection, execute_command_and_log
import random

def process_files(directory_path, key):
    # Connect to the database
    cursor = connect_database()
    
    # Encrypt and decrypt files in the specified directory
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.tif'):
                input_file_path = os.path.join(root, file)
                #output_file_path = os.path.join('fingerprint_dataset_encrypt', file)
                
                # Encrypt the file and save it with the .enc extension
                encrypted_data = encrypt_file(input_file_path, key.encode())
                
                try:
                    # Create a new user
                    insert_user_command = 'INSERT INTO users (username, name, age) VALUES (?, ?, ?)'
                            
                    user_name = generate_random_name()
                    username = "".join([n[0] for n in user_name.split(' ')])
                        
                    # Generate a random user name and age
                    user_params = (username, user_name, random.randint(10, 80))
                    execute_command_and_log(cursor, insert_user_command, user_params)

                    # Get the ID of the newly inserted user
                    user_id = cursor.lastrowid
                        
                    # Insert a fingerprint for the user
                    insert_fingerprint_command = 'INSERT INTO fingerprint (fingerprint_data, user_id) VALUES (?, ?)'
                    fingerprint_params = (encrypted_data, user_id)
                    execute_command_and_log(cursor, insert_fingerprint_command, fingerprint_params)

                    print(f"User '{user_name}', with username '{username}' with ID {user_id} created successfully with a fingerprint.")
                except Exception as e:
                    print(f"Error: {e}")
                    
                #try:
                    # Raenme the encrypted file to the output directory
                #    os.rename(input_file_path + '.enc', output_file_path + '.enc')
                #except Exception as e:
                #    print(f"Error: {e}")
                #    os.remove(input_file_path + '.enc')
    
    # Close DB connection
    close_database_connection()
                    
def generate_random_name():
    # Lists of example first names and last names
    first_names = [
        "Emma", "Liam", "Olivia", "Noah", "Ava",
        "Isabella", "Sophia", "Jackson", "Mia", "Lucas",
        "Aiden", "Ella", "Caden", "Chloe", "Oliver",
        "Charlotte", "Amelia", "Benjamin", "Harper", "Evelyn",
        "Abigail", "Emily", "James", "Mila", "Lily",
        "Avery", "Ethan", "Evelyn", "Liam", "Scarlett",
        "Zoe", "Aria", "Mason", "Grace", "Logan",
        "Alexander", "Sofia", "Riley", "Elijah", "Aubrey",
        "Nora", "Levi", "Hannah", "Samuel", "Aiden"
    ]
    mid_names = [
        "Grace", "Alexander", "Victoria", "James", "Olivia",
        "Daniel", "Sophia", "Michael", "Emily", "William",
        "Elizabeth", "Matthew", "Emma", "David", "Ava",
        "Christopher", "Charlotte", "John", "Ella", "Nicholas",
        "Amelia", "Andrew", "Madison", "Benjamin", "Lily",
        "Jacob", "Abigail", "Christopher", "Sophie", "Ethan",
        "Grace", "Nathan", "Hannah", "Logan", "Avery",
        "Isaac", "Zoe", "Caleb", "Mia", "Ryan",
        "Aria", "Luke", "Aiden", "Lillian", "Carter"
    ]
    last_names = [
        "Smith", "Johnson", "Williams", "Jones", "Brown",
        "Davis", "Miller", "Wilson", "Moore", "Taylor",
        "Anderson", "Thomas", "Jackson", "White", "Harris",
        "Martin", "Thompson", "Garcia", "Martinez", "Robinson",
        "Clark", "Lewis", "Lee", "Walker", "Hall",
        "Allen", "Young", "King", "Wright", "Lopez",
        "Hill", "Scott", "Green", "Adams", "Baker",
        "Gonzalez", "Nelson", "Carter", "Perez", "Taylor",
        "Cooper", "Flores", "Evans", "Morgan", "Ross"
    ]
    
    random_names = [
        "Alice", "Bob", "Charlie", "David", "Emma",
        "Frank", "Grace", "Henry", "Ivy", "Jack",
        "Kate", "Leo", "Mia", "Noah", "Olivia",
        "Peter", "Quinn", "Rachel", "Sam", "Tom",
        "Sophia", "Ethan", "Ava", "Liam", "Isabella",
        "Jackson", "Sophie", "Lucas", "Chloe", "Logan",
        "Madison", "Mason", "Ella", "Caden", "Amelia",
        "Benjamin", "Avery", "William", "Evelyn", "Oliver",
        "Harper", "Daniel", "Lily", "Michael", "Abigail"
    ]
    
    # Generate random first and last names
    random_first_name = random.choice(first_names)
    random_mid_name = random.choice(mid_names)
    random_last_name = random.choice(last_names)
    random_name = random.choice(random_names)

    # Combine first and last names
    random_full_name = f"{random_first_name} {random_name} {random_mid_name} {random_last_name}"

    return random_full_name

def main():
    # Create a new directory to store the encrypted files
    #os.makedirs('fingerprint_dataset_encrypt', exist_ok=True)

    # Generate a key for encryption
    #key = Fernet.generate_key()
    #print(f"key: {key}")

    key = "PqV8juaCaTmXcAXXMIF8qAcuzO2oPzDXKvBXQAkAo40="
    #cipher_suite = Fernet(key)
                
    process_files('fingerprint_dataset', key)
    
if __name__ == "__main__":
    main()