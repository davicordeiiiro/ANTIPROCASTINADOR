from time import sleep
from database.connection import conectar

def iniciar_pomodoro():
    conn = conectar()
    cursor = conn.cursor()

    tarefa_id = input("ID da tarefa: ")
    minutos = int(input("Duração do foco (minutos): "))

    print("Iniciando foco...")
    
    for i in range(minutos, 0, -1):
        print(f"{i} minuto(s) restante(s)")
        sleep(60)

    print("Pomodoro concluído!")

    cursor.execute(
        "INSERT INTO sessoes (tarefa_id, duracao_minutos) VALUES (%s, %s)",
        (tarefa_id, minutos)
    )

    conn.commit()
    cursor.close()
    conn.close()