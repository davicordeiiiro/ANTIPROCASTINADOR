from database.connection import conectar

def criar_tabelas():

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tarefas (
        id INT AUTO_INCREMENT PRIMARY KEY,
        titulo VARCHAR(50) NOT NULL,
        descricao TEXT,
        status VARCHAR(50) DEFAULT 'pendente',
        prioridade VARCHAR(50),
        data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP
    )                                                                            
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sessoes (
        id INT AUTO_INCREMENT PRIMARY KEY,
        tarefa_id INT,
        data DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (tarefa_id) REFERENCES tarefas(id) 
    )
    """)

    conn.commit()
    conn.close()