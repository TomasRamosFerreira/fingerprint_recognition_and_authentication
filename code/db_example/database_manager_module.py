import sqlite3
from datetime import datetime

# Define global variables
conn = None
cursor = None

def connect_database():
    """
    Connect to the SQLite database or create it if not exists.
    Also, create the 'users', 'fingerprint', and 'command_history' tables if they do not exist.
    """
    global conn, cursor
    conn = sqlite3.connect('localdatabase.db')
    cursor = conn.cursor()

    # Create the 'users' table if it does not exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            failed_attempts INTEGER NOT NULL DEFAULT 0,
            bloqued_until DATETIME
        )
    ''')

    # Create the 'fingerprint' table if it does not exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS fingerprint (
            id INTEGER PRIMARY KEY,
            fingerprint_data BLOB NOT NULL,
            user_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')

    # Create the 'command_history' table if it does not exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS command_history (
            id INTEGER PRIMARY KEY,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            command_text TEXT NOT NULL
        )
    ''')

    # Commit the changes
    conn.commit()
    
    return cursor

def create_db_cursor():
    """
    Create a new cursor to the db
    """
    global conn
    
    return conn.cursor()

def close_database_connection():
    """
    Close the connection to the SQLite database.
    """
    global conn
    conn.close()
    
def execute_command_and_log(cursor, command, params=None):
    """
    Execute the given SQL command and store it in the command_history table.
    """
    global conn
    
    if not cursor:
        cursor = create_db_cursor()

    # Log the command in command_history
    timestamp = datetime.now()
    cursor.execute('INSERT INTO command_history (timestamp, command_text) VALUES (?, ?)', (timestamp, command))

    # Execute the command with optional parameters
    if params is not None:
        cursor.execute(command, params)
    else:
        cursor.execute(command)

    # Commit the changes
    conn.commit()
    
def get_database_logs(order="DESC"):
    global cursor
    execute_command_and_log(cursor, f'SELECT * FROM command_history ORDER BY id {order}')
    logs = cursor.fetchall()
    
    for log in logs:
        id, timestamp, command_text = log
        print(f"Time: {timestamp}; Query: {command_text}")