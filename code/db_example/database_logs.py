from database_manager_module import connect_database, close_database_connection, get_database_logs

def main():
    # Connect to the database
    cursor = connect_database()
    
    get_database_logs()
            
    # Close DB connection
    close_database_connection()

if __name__ == "__main__":
    main()