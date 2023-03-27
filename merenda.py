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
