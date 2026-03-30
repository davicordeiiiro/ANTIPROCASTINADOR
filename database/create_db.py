from database.connection import conectar

def criar_tabelas():
    conn = conectar(database=None)
    cursor = conn.cursor()

    cursor.execute("CREATE DATABASE IF NOT EXISTS antiproc")
    cursor.execute("USE antiproc")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tarefas (
        id INT AUTO_INCREMENT PRIMARY KEY,
        titulo VARCHAR(255),
        concluida BOOLEAN DEFAULT FALSE
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sessoes (
        id INT AUTO_INCREMENT PRIMARY KEY,
        tarefa_id INT,
        tecnologia VARCHAR(255),
        duracao_minutos INT,
        data DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (tarefa_id) REFERENCES tarefas(id)
    )
    """)
    
    # Executa verificação para não apagar banco de dados e dar upgrade nele.
    try:
        cursor.execute("ALTER TABLE sessoes ADD COLUMN tecnologia VARCHAR(255) AFTER tarefa_id")
    except Exception as e:
        # Erro 1060 é 'Duplicate column name' o que é o que tentamos evitar se já existir!
        if getattr(e, "errno", None) != 1060:
            pass

    
    conn.commit()
    cursor.close()
    conn.close()