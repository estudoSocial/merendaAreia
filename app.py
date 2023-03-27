import sqlite3
import streamlit as st
import database
import authentication
import merenda

conn = sqlite3.connect('merenda.db')
database.create_tables(conn)

st.title('Controle de Merenda Escolar')
st.subheader('Login')

login_form = st.form(key='login')
usuario = login_form.text_input('Usuário')
senha = login_form.text_input('Senha', type='password')
login_form.form_submit_button('Entrar')

escola_logada = authentication.login(conn, usuario, senha)

if escola_logada:
    st.subheader(f'Estoque atual ({escola_logada})')
    estoque_df = merenda.calcular_estoque(conn, escola_logada)
    st.dataframe(estoque_df)

    form = st.form(key='registrar')
    produto = form.text_input('Produto')
    unidade = form.selectbox('Unidadede medida', options=['Kg', 'L', 'Dz', 'Und', 'Cx'])
    quantidade = form.number_input('Quantidade', min_value=0, step=1)
    procedimento = form.selectbox('Procedimento', options=['Entrada', 'Saída'])
    form.form_submit_button('Registrar')

if produto and quantidade and procedimento:
    merenda.registrar(conn, escola_logada, produto, unidade, quantidade, procedimento)

st.subheader(f'Histórico de Registros ({escola_logada})')
df = merenda.list_records(conn, escola_logada)
st.dataframe(df)
