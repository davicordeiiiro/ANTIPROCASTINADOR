from database.connection import conectar
from datetime import datetime, timedelta

class BancoDados:
    
    def __init__(self):
        self.conn = conectar()
        
    def salvar_progresso(self, tarefa_titulo, tech, minutos):
        # Primeiro acha ou cria a tarefa pelo titulo
        cursor = self.conn.cursor()
        
        cursor.execute("SELECT id FROM tarefas WHERE titulo = ? LIMIT 1", (tarefa_titulo,))
        resultado = cursor.fetchone()
        
        if resultado:
            tarefa_id = resultado[0]
        else:
            cursor.execute("INSERT INTO tarefas (titulo) VALUES (?)", (tarefa_titulo,))
            self.conn.commit()
            tarefa_id = cursor.lastrowid
            
        cursor.execute(
            "INSERT INTO sessoes (tarefa_id, tecnologia, duracao_minutos) VALUES (?, ?, ?)",
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
        WHERE data >= ? AND tecnologia IS NOT NULL
        GROUP BY tecnologia
        """
        # Formata a data para string ISO pois o SQLite lida melhor com comparações de string em datas
        cursor.execute(query, (ultima_semana.strftime('%Y-%m-%d %H:%M:%S'),))
        resultados = cursor.fetchall()
        cursor.close()
        return resultados
