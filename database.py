import sqlite3
from sqlite3 import Error

database = 'cars.db'

def create_connection():
    conn = None
    try:
        conn = sqlite3.connect(database)
        print(f'Successfully connected to SQLite database: {database}')
    except Error as e:
        print(e)

    return conn

def create_table(conn):
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS cars (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        year INTEGER NOT NULL,
        description TEXT,
        price REAL,
        image TEXT
    );
    '''

    try:
        cursor = conn.cursor()
        cursor.execute(create_table_query)
        print('Table created successfully')
    except Error as e:
        print(e)
