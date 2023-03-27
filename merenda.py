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

def calcular_estoque(conn, escola):
    df = list_records(conn, escola)
    entradas = df[df['procedimento'] == 'Entrada'].groupby('produto').sum()
    saidas = df[df['procedimento'] == 'Saída'].groupby('produto').sum()
    estoque = entradas - saidas
    return estoque.fillna(0)

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
    cursor = conn.execute('SELECT * FROM entregas_pendentes WHERE id = ?', (id,))
    entrega = cursor.fetchone()

    if entrega:
        escola, produto, unidade, quantidade = entrega[1], entrega[3], entrega[4], entrega[5]
        atualizar_estoque(escola, produto, unidade, quantidade)
        conn.execute('UPDATE entregas_pendentes SET status = ? WHERE id = ?', ('entregue', id))
        conn.commit()

    
def atualizar_estoque(escola, produto, unidade, quantidade):
    cursor = conn.execute('SELECT quantidade FROM estoque WHERE escola = ? AND produto = ? AND unidade = ?', (escola, produto, unidade))
    data = cursor.fetchone()
    
    if data:
        nova_quantidade = data[0] + quantidade
        conn.execute('UPDATE estoque SET quantidade = ? WHERE escola = ? AND produto = ? AND unidade = ?', (nova_quantidade, escola, produto, unidade))
    else:
        conn.execute('INSERT INTO estoque (escola, produto, unidade, quantidade) VALUES (?, ?, ?, ?)', (escola, produto, unidade, quantidade))
    
    conn.commit()

    def registrar_entrega_pendente(escola, produto, unidade, quantidade):
    status = 'aguardando'
    conn.execute('INSERT INTO entregas_pendentes (escola, produto, unidade, quantidade, status) VALUES (?, ?, ?, ?, ?)',
                 (escola, produto, unidade, quantidade, status))
    conn.commit()

