#!/usr/bin/env python3
import streamlit as st
import sqlite3
import base64

# Defina o caminho para o arquivo do banco de dados SQLite
db_path = 'merenda.db'

# Função para fazer o download do arquivo do banco de dados
def download_db_file():
    with open(db_path, 'rb') as f:
        file_content = f.read()
        file_name = 'backup.db'
        base64_encoded_file = base64.b64encode(file_content).decode('utf-8')
        href = f'<a href="data:application/octet-stream;base64,{base64_encoded_file}" download="{file_name}">Clique aqui para baixar o arquivo de backup</a>'
        return href

# Função para restaurar um arquivo de backup
def restore_backup(backup_file):
    # Feche a conexão com o banco de dados antes de restaurar o backup
    conn.close()
    # Copie o arquivo de backup para o diretório do banco de dados
    shutil.copy(backup_file, db_path)
    # Abra uma nova conexão com o banco de dados restaurado
    conn = sqlite3.connect(db_path)

# Função para adicionar a funcionalidade de backup e restauração para a escola SEDUC
def add_backup_functionality(streamlit):
    escola = streamlit.session_state.escola_logada
    if escola == 'SEDUC':
        # Adicione uma opção de download e upload no aplicativo
        streamlit.subheader('Backup do banco de dados')
        streamlit.markdown(download_db_file(), unsafe_allow_html=True)
        #backup_file = streamlit.file_uploader('Faça o upload de um arquivo de backup', type='db')
        #if backup_file is not None:
        #    restore_backup(backup_file.name)
        #    streamlit.success(f'O arquivo {backup_file.name} foi restaurado com sucesso')
