from database.connection import conectar

def deletar_tarefa():
    conn = conectar()
    cursor = conn.cursor()

    id_tarefa = input("ID da tarefa para deletar: ")

    cursor.execute("DELETE FROM tarefas WHERE id = %s", (id_tarefa,))
    conn.commit()

    print("Tarefa deletada com sucesso!")

    cursor.close()
    conn.close()