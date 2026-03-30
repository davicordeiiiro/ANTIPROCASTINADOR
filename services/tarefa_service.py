from database.connection import conectar
from models.tarefa import Tarefa

from database.connection import conectar
from models.tarefa import Tarefa


def buscar_tarefas():

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT id, titulo, descricao, status FROM tarefas")

    resultados = cursor.fetchall()

    tarefas = []

    for r in resultados:
        tarefa = Tarefa(r[0], r[1], r[2], r[3])
        tarefas.append(tarefa)

    cursor.close()
    conn.close()

    return tarefas