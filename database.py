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
        escola TEXT,
        data TEXT,
        produto TEXT,
        unidade TEXT,
        quantidade REAL,
        status TEXT
    )
''')

def add_default_seduc_user(conn):
    cursor = conn.execute('SELECT * FROM usuarios WHERE usuario="departamento.merenda"')
    if cursor.fetchone() is None:
        conn.execute('INSERT INTO usuarios (usuario, senha, escola) VALUES (?, ?, ?)',
                     ("departamento.merenda", "arrozcomcarnenoprato", "SEDUC"))
        conn.commit()
        
def registrar_entrega_pendente(escola, produto, unidade, quantidade):
    data = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
    conn.execute('INSERT INTO entregas_pendentes (escola, data, produto, unidade, quantidade, status) VALUES (?, ?, ?, ?, ?, ?)',
                 (escola, data, produto, unidade, quantidade, 'esperando entrega'))
    conn.commit()

def listar_entregas_pendentes(escola):
    cursor = conn.execute('SELECT * FROM entregas_pendentes WHERE escola = ? AND status = ?', (escola, 'esperando entrega'))
    data = cursor.fetchall()
    df = pd.DataFrame(data, columns=['id', 'escola', 'data', 'produto', 'unidade', 'quantidade', 'status'])
    return df

def aceitar_entrega(id):
    conn.execute('UPDATE entregas_pendentes SET status = ? WHERE id = ?', ('entregue', id))
    conn.commit()

