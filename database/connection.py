import mysql.connector

def conectar(database="antiproc"):
    config = {
        "host": "localhost",
        "user": "root",
        "password": ""
    }
    if database:
        config["database"] = database
        
    conn = mysql.connector.connect(**config)
    return conn