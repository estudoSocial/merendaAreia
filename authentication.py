import pandas as pd

def login(conn, usuario, senha):
    cursor = conn.execute('SELECT escola FROM usuarios WHERE usuario=? AND senha=?', (usuario, senha))
    escola = cursor.fetchone()
    return escola[0] if escola else None

def create_user(conn, usuario, senha, escola):
    conn.execute('INSERT INTO usuarios (usuario, senha, escola) VALUES (?, ?, ?)', (usuario, senha, escola))
    conn.commit()

def edit_user(conn, usuario, new_usuario, new_senha, new_escola):
    conn.execute('UPDATE usuarios SET usuario=?, senha=?, escola=? WHERE usuario=?', (new_usuario, new_senha, new_escola, usuario))
    conn.commit()

def delete_user(conn, usuario):
    conn.execute('DELETE FROM usuarios WHERE usuario=?', (usuario,))
    conn.commit()

def list_users(conn):
    cursor = conn.execute('SELECT * FROM usuarios')
    data = cursor.fetchall()
    df = pd.DataFrame(data, columns=['id', 'usuario', 'senha', 'escola'])
    return df
