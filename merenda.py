import pandas as pd

def registrar(conn, escola, produto, unidade, quantidade, procedimento):
    data = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
    conn.execute('INSERT INTO merenda (escola, data, produto, unidade, quantidade, procedimento) VALUES (?, ?, ?, ?, ?, ?)',
                (escola, data, produto, unidade, quantidade, procedimento))
    
    # Ajustar a quantidade com base no procedimento (entrada ou saída)
    quantidade_ajustada = quantidade if procedimento == 'entrada' else -quantidade
    
    # Atualizar o estoque
    atualizar_estoque(conn, escola, produto, unidade, quantidade_ajustada)
    
    # Confirmar as alterações
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
    
def deletar_registro(conn, id):
    conn.execute('DELETE FROM merenda WHERE id = ?', (id,))
    conn.commit()


def listar_entregas_pendentes(conn, escola):
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

    
def atualizar_estoque(conn, escola, produto, unidade, quantidade_ajustada):
    cursor = conn.execute('SELECT quantidade FROM estoque WHERE escola = ? AND produto = ? AND unidade = ?', (escola, produto, unidade))
    resultado = cursor.fetchone()

    if resultado:
        nova_quantidade = resultado[0] + quantidade_ajustada
        conn.execute('UPDATE estoque SET quantidade = ? WHERE escola = ? AND produto = ? AND unidade = ?', (nova_quantidade, escola, produto, unidade))
    else:
        conn.execute('INSERT INTO estoque (escola, produto, unidade, quantidade) VALUES (?, ?, ?, ?)', (escola, produto, unidade, quantidade_ajustada))

    conn.commit()


def registrar_entrega_pendente(escola, produto, unidade, quantidade):
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'merenda.db')
    conn = sqlite3.connect(db_path)

    data = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
    conn.execute('INSERT INTO entregas_pendentes (escola, data, produto, unidade, quantidade, status) VALUES (?, ?, ?, ?, ?, ?)',
                 (escola, data, produto, unidade, quantidade, 'esperando entrega'))
    conn.commit()

    conn.close()  # Adicione esta linha para fechar a conexão
    



