import mysql.connector #biblioteca que eu baixei para interpretar mysql no python

def conectar():
    conn = mysql.connector.connect(
        host="localhost",
        user="antiproc_user",
        password="1234",
        database="antiproc"
    )

    return conn