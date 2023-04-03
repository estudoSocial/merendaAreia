import sqlite3
import streamlit as st
import database
import authentication
import merenda
import pandas as pd
import os
from backup import add_backup_functionality

conn = sqlite3.connect('merenda.db')

# Inicializar a variável de estado do procedimento selecionado, se ainda não existir
if "procedimento" not in st.session_state:
    st.session_state.procedimento = "Entrada"

database.create_tables(conn)
database.add_default_seduc_user(conn)
escola_logada = None

# Verifique se 'escola_logada' existe no session_state, caso contrário, defina como None
if "escola_logada" not in st.session_state:
    st.session_state.escola_logada = None

if not st.session_state.escola_logada:
    st.subheader("Login")
    usuario = st.text_input("Nome de usuário")
    senha = st.text_input("Senha", type="password")
    login_button = st.button("Entrar")

    if login_button:
        st.session_state.escola_logada = authentication.login(conn, usuario, senha)

if st.session_state.escola_logada:
    lista_de_escolas = [
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
    "Escola Ver. Nelson Carneiro",
    "Escola Fulano de Teste"
    ]

    if st.session_state.escola_logada != 'SEDUC':
        st.title('Sistema de Registros de Merenda de Areia - PB')
        st.subheader(f'{st.session_state.escola_logada}')
        with st.expander(f"Entregas pendentes para {st.session_state.escola_logada}"):
            entregas_df = merenda.listar_entregas_pendentes(conn, st.session_state.escola_logada)

            for index, row in entregas_df.iterrows():
                st.write(f"{row['produto']} - {row['quantidade']} {row['unidade']}")
                if st.button(f"aceitar entrega {row['id']}"):
                    merenda.aceitar_entrega(conn, row['id'])
                    st.success("entrega aceita")


        with st.expander('Adicionar Novo Registro de Entrada ou Saída.'):
            form = st.form(key='registrar',clear_on_submit=True)

            # Selecione o procedimento
            procedimento = form.selectbox('Procedimento', options=['Entrada', 'Saída'])
            produto = form.text_input("Produto").strip().upper()
            unidade = form.selectbox('Unidadede medida', options=['Kg', 'L', 'Dz', 'Und', 'Cx'])
            quantidade = form.number_input('Quantidade', min_value=0.0, step=1.0)
            form_submit_record = form.form_submit_button('Registrar')

            if form_submit_record:
                if produto and quantidade and procedimento:
                    if procedimento == 'Saída':
                        saldo_estoque = merenda.verificar_estoque(conn, st.session_state.escola_logada, produto)
                        if saldo_estoque < quantidade:
                            st.error('Saldo insuficiente no estoque')
                        else:
                            merenda.registrar(conn, st.session_state.escola_logada, produto, unidade, quantidade, procedimento)
                            estoque_df = merenda.estoque_atual(conn, st.session_state.escola_logada)
                            st.success("Registro adicionado com sucesso")
                            st.experimental_rerun()  # Adicione esta linha
                    else:
                        merenda.registrar(conn, st.session_state.escola_logada, produto, unidade, quantidade, procedimento)
                        estoque_df = merenda.estoque_atual(conn, st.session_state.escola_logada)
                        st.success("Registro adicionado com sucesso")
                        st.experimental_rerun()  # Adicione esta linha
                else:
                    merenda.registrar(conn, st.session_state.escola_logada, produto, unidade, quantidade, procedimento)
                    merenda.atualizar_estoque(conn, st.session_state.escola_logada, produto, procedimento, quantidade)
                    estoque_df = merenda.estoque_atual(conn, st.session_state.escola_logada)
                    st.success("Registro adicionado com sucesso")
                    st.experimental_rerun()  # Adicione esta linha

        with st.expander(f'Deletar Registros da {st.session_state.escola_logada}'):
            df = merenda.list_records(conn, st.session_state.escola_logada)

            if not df.empty:
                # Adicionando a funcionalidade de exclusão
                delete_form = st.form(key='delete_form', clear_on_submit=True)
                delete_id = delete_form.selectbox('Selecione o registro para excluir, verifique o ID (identificador) antes de excluí-lo)',
                                                  options=[(row['id'], row['produto'], row['quantidade'], row['unidade'], row['procedimento']) for _, row in df.iterrows()],
                                                  format_func=lambda x: f"ID: {x[0]} | {x[1]} - {x[2]} {x[3]} | {x[4]}")
                delete_button = delete_form.form_submit_button("Excluir registro")

                if delete_button:
                    merenda.delete_record(conn, delete_id[0])
                    # Atualize o estoque, se necessário
                    st.success(f"Registro {delete_id[0]} excluído com sucesso")
                    df = merenda.list_records(conn, st.session_state.escola_logada)  # Atualize o DataFrame após excluir um registro
                    st.experimental_rerun()
            else:
                st.write("Nenhum registro encontrado.")

        with st.expander('Histórico de Registros de Entrada e Saída'):
            st.dataframe(df)

        with st.expander(f'Estoque atual ({st.session_state.escola_logada})'):
            estoque_df = merenda.estoque_atual(conn, st.session_state.escola_logada)
            st.dataframe(estoque_df)

    if st.session_state.escola_logada == 'SEDUC':
        st.title('Sistema de Gestão de Merenda de Areia - PB')
        st.subheader(f'{st.session_state.escola_logada}')
        with st.expander(f"Criar Entrega"):
            st.subheader("Enviar produtos para a escola")
            escola_destino = st.selectbox("Escola", options=lista_de_escolas) # use a lista de escolas definida anteriormente
            produto = st.text_input("Produto").strip().upper()
            unidade = st.selectbox("Unidade de medida", options=['Kg', 'L', 'Dz', 'Und', 'Cx'])
            quantidade = st.number_input("Quantidade", min_value=0.0, step=1.0)
            enviar_button = st.button("Enviar")

            if enviar_button and produto and quantidade:
                merenda.registrar_entrega_pendente(escola_destino, produto, unidade, quantidade)
                st.success("Produto enviado para a escola")

        with st.expander(f"Criar Usuários"):
            st.subheader('Criar Novo Usuário')

            form = st.form(key='create_user_form',clear_on_submit=True)
            new_username = form.text_input('Nome de usuário')
            new_password = form.text_input('Senha', type='password')
            new_school = form.selectbox('Escola', options=lista_de_escolas + ['SEDUC'])
            create_button = form.form_submit_button('Criar Usuário')

            if create_button and new_username and new_password and new_school:
                authentication.create_user(conn, new_username, new_password, new_school)
                users_df = authentication.list_users(conn)
                st.success(f'Usuário {new_username} criado com sucesso')
            elif create_button:
                st.error('Preencha todos os campos')

        with st.expander(f'Deletar Usuários'):
            # Listar todos os usuários cadastrados com botão de exclusão
            st.subheader('Lista de Usuários')
            users_df = authentication.list_users(conn)
            for i, row in users_df.iterrows():
                user = row['usuario'] + " da " + row['escola']
                key = f'erase_user_{i}'
                delete_button = st.button(f'Excluir {user}', key=key)
                if delete_button:
                    authentication.delete_user(conn, row['usuario'])
                    st.success(f'O usuário {user} foi excluído com sucesso')
            # Atualizar a lista de usuários após exclusão
            users_df = authentication.list_users(conn)

        with st.expander('Clique aqui para ver o banco de dados de usuários'):
            users_df = authentication.list_users(conn)
            st.dataframe(users_df)


        with st.expander('Clique aqui para baixar uma cópia do banco de dados dos registros de merenda'):
            add_backup_functionality(st)

with st.expander('Deseja deslogar?'):
    if st.button('Clique aqui para sair.', key='sair_button'):
        st.session_state.escola_logada = None
        st.experimental_rerun()
