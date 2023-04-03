import pandas as pd

def registrar(conn, escola, produto, unidade, quantidade, procedimento):
    data = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
    conn.execute('INSERT INTO merenda (escola, data, produto, unidade, quantidade, procedimento) VALUES (?, ?, ?, ?, ?, ?)',
                (escola, data, produto, unidade, quantidade, procedimento))
    conn.commit()

def list_records(conn, escola):
    cursor = conn.execute('SELECT * FROM merenda WHERE escola=?', (escola,))
    data = cursor.fetchall()
    df = pd.DataFrame(data, columns=['id', 'escola', 'data', 'produto', 'unidade', 'quantidade', 'procedimento'])
    return df

def delete_record(conn, id):
    conn.execute('DELETE FROM merenda WHERE id = ?', (id,))
    conn.commit()

def estoque_atual(conn, escola):
    cursor = conn.cursor()
    query = """
    SELECT produto, unidade, SUM(CASE WHEN procedimento = 'Entrada' THEN quantidade ELSE -quantidade END) as saldo
    FROM merenda
    WHERE escola = ?
    GROUP BY produto, unidade
    """
    cursor.execute(query, (escola,))
    estoque_df = pd.DataFrame(cursor, columns=['produto', 'unidade', 'saldo'])
    return estoque_df

def verificar_estoque(conn, escola, produto):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT SUM(CASE
            WHEN procedimento = 'Entrada' THEN quantidade
            ELSE -quantidade
        END) as saldo
        FROM merenda
        WHERE produto = ? AND escola = ?;
    """, (produto, escola))
    row = cursor.fetchone()
    return row[0] if row[0] is not None else 0

def atualizar_estoque(conn, escola, produto, procedimento, quantidade):
    cursor = conn.cursor()
    # Verificar a quantidade atual no estoque
    cursor.execute("SELECT quantidade FROM merenda WHERE escola=? AND produto=?", (escola, produto))
    resultado = cursor.fetchone()
    if resultado:
        estoque_atual = resultado[0]
    else:
        estoque_atual = 0
    # Atualizar o estoque com base no procedimento
    if procedimento == 'Entrada':
        estoque_atual += quantidade
    else:
        estoque_atual -= quantidade
    # Atualizar o estoque no banco de dados (supondo que você tenha uma tabela separada para armazenar o estoque)
    if resultado:
        cursor.execute("UPDATE merenda SET quantidade=? WHERE escola=? AND produto=?", (estoque_atual, escola, produto))
    else:
        cursor.execute("INSERT INTO merenda (escola, produto, quantidade) VALUES (?, ?, ?)", (escola, produto, estoque_atual))
    conn.commit()

def produtos_em_estoque(conn, escola):
    cursor = conn.execute('SELECT produto FROM merenda WHERE escola = ? AND quantidade > 0 GROUP BY produto', (escola,))
    produtos = cursor.fetchall()
    return [item[0] for item in produtos]

def registrar_entrega_pendente(escola, produto, unidade, quantidade):
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'merenda.db')
    conn = sqlite3.connect(db_path)

    data = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
    conn.execute('INSERT INTO entregas_pendentes (escola, data, produto, unidade, quantidade, status) VALUES (?, ?, ?, ?, ?, ?)',
                 (escola, data, produto, unidade, quantidade, 'esperando entrega'))
    conn.commit()
    conn.close()  # Adicione esta linha para fechar a conexão

def registrar_entrega_pendente(escola, produto, unidade, quantidade):
    data = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
    conn.execute('INSERT INTO entregas_pendentes (escola, data, produto, unidade, quantidade, status) VALUES (?, ?, ?, ?, ?, ?)',
                 (escola, data, produto, unidade, quantidade, 'esperando entrega'))
    conn.commit()
    
def listar_entregas_pendentes(conn, escola):
    cursor = conn.execute('SELECT * FROM entregas_pendentes WHERE escola = ? AND status = ?', (escola, 'esperando entrega'))
    data = cursor.fetchall()
    df = pd.DataFrame(data, columns=['id', 'escola', 'data', 'produto', 'unidade', 'quantidade', 'status'])
    return df

def aceitar_entrega(conn, id):
    cursor = conn.execute('SELECT * FROM entregas_pendentes WHERE id = ?', (id,))
    entrega = cursor.fetchone()
    if entrega:
        escola, produto, unidade, quantidade = entrega[1], entrega[3], entrega[4], entrega[5]
        atualizar_estoque(escola, produto, unidade, quantidade)
        conn.execute('UPDATE entregas_pendentes SET status = ? WHERE id = ?', ('entregue', id))
        conn.commit()
