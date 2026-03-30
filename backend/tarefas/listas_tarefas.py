from database.connection import conectar
from services.tarefa_service import buscar_tarefas

def listar_tarefas():

    tarefas = buscar_tarefas()

    for tarefa in tarefas:
        print(f"{tarefa.id} - {tarefa.titulo} - {tarefa.status}")

def listas_tarefas():

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tarefas")

    tarefas = cursor.fetchall()

    print("\n===== SUAS TAREFAS =====")

    if not tarefas:
        print("Nenhuma tarefa encontrada")

    for tarefa in tarefas:
        print(f"ID: {tarefa[0]}")
        print(f"Título: {tarefa[1]}")
        print(f"Descrição: {tarefa[2]}")
        print(f"Status: {tarefa[3]}")
        print(f"Prioridade: {tarefa[4]}")
        print("-----------------------")


    cursor.close()
    conn.close()

    