from database.connection import conectar

def criar_tabelas():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tarefas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo VARCHAR(255),
        concluida BOOLEAN DEFAULT 0
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sessoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tarefa_id INTEGER,
        tecnologia VARCHAR(255),
        duracao_minutos INTEGER,
        data DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (tarefa_id) REFERENCES tarefas(id)
    )
    """)

    conn.commit()
    cursor.close()
    conn.close()