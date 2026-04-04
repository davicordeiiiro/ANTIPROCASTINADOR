import sqlite3

def conectar(database="antiproc.db"):
    # Conecta ou cria o arquivo "antiproc.db" na mesma aba/app
    # O check_same_thread=False ajuda com eventos no Flet / Assíncrono
    conn = sqlite3.connect(database, check_same_thread=False)
    return conn