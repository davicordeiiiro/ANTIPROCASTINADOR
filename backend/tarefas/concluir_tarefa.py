from database.connection import conectar

def concluir_tarefa(id_tarefa):

    conn = conectar()
    cursor = conn.cursor()

    sql = """
    UPDATE tarefas
    SET status = 'concluida'
    WHERE id = %s
    """

    cursor.execute(sql, (id_tarefa,))

    conn.commit()

    cursor.close()
    conn.close()