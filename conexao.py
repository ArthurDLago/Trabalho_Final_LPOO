import psycopg2

def conectar():
    return psycopg2.connect(
        host="localhost",
        database="Trabalho_Final_LPOO",
        user="postgres",
        password="postgres"
    )