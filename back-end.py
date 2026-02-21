import sqlite3
from datetime import datetime

class BancoDados:
    def __init__(self):
        # check_same_thread=False é essencial para o Flet (que usa threads)
        self.conn = sqlite3.connect("antiprocastinador.db", check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.cria_tabela()

    def cria_tabela(self):
        """Cria a tabela se ela não existir ao iniciar o app."""
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS tarefas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tarefa TEXT NOT NULL,
                tech TEXT NOT NULL,
                minutos INTEGER NOT NULL,
                date DATE NOT NULL
            )
        """)      
        self.conn.commit()

    def salvar_progresso(self, tarefa, tech, minutos):
        """Insere um novo ciclo de foco no banco de dados."""
        data_hoje = datetime.now().strftime("%Y-%m-%d")
        self.cursor.execute(
            "INSERT INTO tarefas (tarefa, tech, minutos, date) VALUES (?, ?, ?, ?)",
            (tarefa, tech.upper(), minutos, data_hoje) # Salva tech em maiúsculo para padronizar
        )
        self.conn.commit()
    
    def obter_relatorio_semanal(self):
        """Retorna o total de minutos por tecnologia dos últimos 7 dias."""
        self.cursor.execute("""
            SELECT tech, SUM(minutos) 
            FROM tarefas 
            WHERE date >= date('now', '-7 days')
            GROUP BY tech 
            ORDER BY SUM(minutos) DESC
        """)
        return self.cursor.fetchall()

    def fechar_conexão(self):
        """Fecha a conexão com o banco com segurança."""
        self.conn.close()
