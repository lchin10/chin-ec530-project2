import sqlite3

def create_database():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS Users")
    cursor.execute("DROP TABLE IF EXISTS Files")
    cursor.execute("DROP TABLE IF EXISTS Metadata")

    # Users
    cursor.execute('''
        CREATE TABLE Users (
            U_ID INTEGER PRIMARY KEY,
            Username TEXT,
            Hashed_password TEXT,
            NOFiles INTEGER
        )
    ''')

    # Files
    cursor.execute('''
        CREATE TABLE Files (
            files_ID INTEGER PRIMARY KEY,
            file_title TEXT,
            file_data BLOB,
            U_ID INTEGER,
            FOREIGN KEY(U_ID) REFERENCES Users(U_ID)
        )
    ''')

    # Metadata
    cursor.execute('''
        CREATE TABLE Metadata (
            file_ID INTEGER,
            length INTEGER,
            width INTEGER,
            type TEXT,
            FOREIGN KEY(file_ID) REFERENCES Files(files_ID)
        )
    ''')

    # Commit changes and close connection
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_database()
    print('Database cleared.')
    print("Database created successfully.")
