def login(conn, usuario, senha):
    cursor = conn.execute('SELECT escola FROM usuarios WHERE usuario=? AND senha=?', (usuario, senha))
    escola = cursor.fetchone()
    return escola[0] if escola else None
