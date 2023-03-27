import sqlite3
import streamlit as st
import database
import authentication
import merenda

conn = sqlite3.connect('merenda.db')
database.create_tables(conn)
database.add_default_seduc_user(conn)
escola_logada = None

if not escola_logada:
    st.subheader("Login")
    usuario = st.text_input("Nome de usuário")
    senha = st.text_input("Senha", type="password")
    login_button = st.button("Entrar")

    if login_button:
        escola_logada = authentication.login(conn, usuario, senha)

if escola_logada:

    st.subheader(f'Estoque atual ({escola_logada})')
    estoque_df = merenda.calcular_estoque(conn, escola_logada)
    st.dataframe(estoque_df)
    form = st.form(key='registrar')
    st.subheader('Adicionar Novo Registro')
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
    
    if escola_logada == "SEDUC":
        st.subheader('Gerenciar Usuários')

        user_management_form = st.form(key='user_management')
        user_action = user_management_form.radio('Ação', options=['Criar', 'Editar', 'Excluir'])
        target_user = user_management_form.text_input('Nome de usuário alvo')
        new_username = user_management_form.text_input('Novo nome de usuário (se aplicável)')
        new_password = user_management_form.text_input('Nova senha (se aplicável)', type='password')
        new_school = user_management_form.selectbox('Escola (se aplicável)', options=[
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
            "Escola Júlia Verônica dos SantosLeal",
            "Escola Madre Trautlinde",
            "Escola Maria Emília Maracajá",
            "Escola Nenen Silva",
            "Escola Pedro Honório",
            "Escola Lúcia Giovanna",
            "Escola Ver. Nelson Carneiro",
            "SEDUC"
            ])
        user_management_form.form_submit_button('Executar')

        if user_action and target_user:
            if user_action == 'Criar':
                if new_username and new_password and new_school:
                    authentication.create_user(conn, new_username, new_password, new_school)
                    st.success(f'Usuário {new_username} criado com sucesso')
                else:
                    st.error('Preencha todos os campos')
            elif user_action == 'Editar':
                if new_username or new_password or new_school:
                    authentication.edit_user(conn, target_user, new_username, new_password, new_school)
                    st.success(f'Usuário {target_user} editado com sucesso')
                else:
                    st.error('Preencha pelo menos um campo')
            elif user_action == 'Excluir':
                authentication.delete_user(conn, target_user)
                st.success(f'Usuário {target_user} excluído com sucesso')
                st.subheader('Lista de Usuários')
                users_df = authentication.list_users(conn)
                st.dataframe(users_df)
            else:
                st.error('Nome de usuário ou senha incorretos')
    
    if st.button('Sair', key='sair_button'):
        escola_logada = None
        st.experimental_rerun()
