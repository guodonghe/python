import sqlite3

class DatabaseConnection:
    def __init__(self,db_name):
        self.db_name = db_name
        self.connection = None

    def __enter__(self):
        self.connection = sqlite3.connect(self.db_name)
        return self.connection

    def __exit__(self,exc_type,exc_val,exc_tb):
        if self.connection:
            if exc_type is None:
                self.connection.commit()
            else:
                self.connection.rollback()
            self.connection.close()


with DatabaseConnection('example.db') as conn:
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)')
    cursor.execute('INSERT INTO users (name) VALUES (?)',('Alice',))
    cursor.execute('INSERT INTO users (name) VALUES (?)',('Bob',))

---------------------------------------------------------------------------------------------------------

import sqlite3

def query_database(db_name,query):
    conn = sqlite3.connect(db_name)
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            print(row)
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()

query = "SELECT * FROM users"

query_database('example.db',query)


