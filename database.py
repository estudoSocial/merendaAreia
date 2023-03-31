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
    
    conn.execute('''
    CREATE TABLE IF NOT EXISTS entregas_pendentes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        escola TEXT NOT NULL,
        produto TEXT NOT NULL,
        unidade TEXT NOT NULL,
        quantidade INTEGER NOT NULL,
        status TEXT NOT NULL
        )
    ''')

def add_default_seduc_user(conn):
    cursor = conn.execute('SELECT * FROM usuarios WHERE usuario="departamento.merenda"')
    if cursor.fetchone() is None:
        conn.execute('INSERT INTO usuarios (usuario, senha, escola) VALUES (?, ?, ?)',
                     ("departamento.merenda", "arrozcomcarnenoprato", "SEDUC"))
        conn.commit()

