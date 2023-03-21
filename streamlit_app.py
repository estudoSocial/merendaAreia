import sqlite3
import streamlit as st
import pandas as pd
import base64

# cria a conexão com o banco de dados
conn = sqlite3.connect('merenda.db')

# cria a tabela se ela não existir
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

# função para registrar uma entrada ou saída na tabela
def registrar(escola, produto, unidade, quantidade, procedimento):
    data = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
    conn.execute('INSERT INTO merenda (escola, data, produto, unidade, quantidade, procedimento) VALUES (?, ?, ?, ?, ?, ?)',
                (escola, data, produto, unidade, quantidade, procedimento))
    conn.commit()

# função para listar os registros da tabela
def list_records():
    cursor = conn.execute('SELECT * FROM merenda')
    data = cursor.fetchall()
    df = pd.DataFrame(data, columns=['id', 'escola', 'data', 'produto', 'unidade', 'quantidade', 'procedimento'])
    return df

# função para baixar os dados em CSV
def download_csv():
    code = st.text_input('Insira o código para baixar os dados em CSV:')
    if code == 'pergunteparaedilene':  # aqui você pode usar o código que desejar
        df = list_records()
        csv = df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="dados.csv">Download CSV</a>'
        return href
    elif code:
        st.error('Código inválido')
    return None

# define o título do aplicativo
st.title('Controle de Merenda Escolar')

# cria o formulário para registrar uma entrada ou saída de produto
form = st.form(key='registrar')
escola = form.selectbox('Escola', options=[
   "Creche André Ricardo Perazzo da Costa",
   "Creche Corina Barreto de Brito Lira",
   "Creche Dona Dina",
   "Creche Ephigênio Barbosa",
   "Creche Ezilda Milanez",
   "Creche José Alves do Nascimento",
   "Escola Abel Barbosa da Silva",
   "Escola Dr. José Inácio de Miranda Pereira",
   "Escola João César",
   "Escola José Lins Sobrinho",
   "Escola José Rodrigues",
   "Escola Júlia Verônica dos Santos Leal",
   "Escola Madre Trautlinde",
   "Escola Maria Emília Maracajá",
   "Escola Nenen Silva",
   "Escola Pedro Honório",
   "Escola Lúcia Giovanna",
   "Escola Ver. Nelson Carneiro"
])
produto = form.text_input('Produto')
unidade = form.selectbox('Unidade de medida', options=['Kg', 'L', 'Dz', 'Und', 'Cx'])
quantidade = form.number_input('Quantidade', min_value=0, step=1)
procedimento = form.selectbox('Procedimento', options=['Entrada', 'Saída'])
form.form_submit_button('Registrar')

# registra a entrada ou saída quando o botão é clicado
if produto and quantidade and procedimento:
    registrar(escola, produto, unidade, quantidade, procedimento)

# exibe o histórico de registros e adiciona o botão para download dos dados em CSV
st.subheader('Histórico de Registros')
df = list_records()
st.dataframe(df)
st.markdown(download_csv(), unsafe_allow_html=True)
