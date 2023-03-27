import sqlite3

def create_tables(conn):
    conn.execute('''
        CREATE TABLE IF NOT EXISTS merenda (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            escola TEXT,
            data TEXT,
            produto TEXT,
            unidade TEXT,
            quantidade REAL,
            procedimento TEXT
        )
    ''')

    conn.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT,
            senha TEXT,
            escola TEXT
        )
    ''')
