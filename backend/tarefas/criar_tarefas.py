from database.connection import conectar

def criar_tarefas(titulo, descricao, prioridade):

    conn = conectar()
    cursor = conn.cursor()

    sql = """
    INSERT INTO tarefas (titulo, descricao, prioridade)
    VALUES (%s, %s, %s)
    """

    cursor.execute(sql, (titulo, descricao, prioridade))

    conn.commit()

    cursor.close()
    conn.close()