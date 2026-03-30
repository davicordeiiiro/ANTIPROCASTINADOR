from database.connection import conectar
from datetime import datetime, timedelta

class BancoDados:
    
    def __init__(self):
        self.conn = conectar()
        
    def salvar_progresso(self, tarefa_titulo, tech, minutos):
        # Primeiro acha ou cria a tarefa pelo titulo
        cursor = self.conn.cursor()
        
        cursor.execute("SELECT id FROM tarefas WHERE titulo = %s LIMIT 1", (tarefa_titulo,))
        resultado = cursor.fetchone()
        
        if resultado:
            tarefa_id = resultado[0]
        else:
            cursor.execute("INSERT INTO tarefas (titulo) VALUES (%s)", (tarefa_titulo,))
            self.conn.commit()
            tarefa_id = cursor.lastrowid
            
        cursor.execute(
            "INSERT INTO sessoes (tarefa_id, tecnologia, duracao_minutos) VALUES (%s, %s, %s)",
            (tarefa_id, tech, minutos)
        )
        self.conn.commit()
        cursor.close()
        
    def obter_relatorio_semanal(self):
        cursor = self.conn.cursor()
        ultima_semana = datetime.now() - timedelta(days=7)
        
        query = """
        SELECT tecnologia, SUM(duracao_minutos) as total
        FROM sessoes
        WHERE data >= %s AND tecnologia IS NOT NULL
        GROUP BY tecnologia
        """
        cursor.execute(query, (ultima_semana,))
        resultados = cursor.fetchall()
        cursor.close()
        return resultados
