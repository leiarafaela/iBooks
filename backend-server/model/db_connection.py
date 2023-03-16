import mysql.connector
from dotenv import load_dotenv
from contextlib import closing
import os


load_dotenv()


user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
host = os.getenv('DB_HOST')
database = os.getenv('DB_DATABASE')


def conectar_mysql():
    conn = mysql.connector.connect(
        user=user,
        password=password,
        host=host,
        database=database
    )

    return conn

def db_criar_clientes(nome, email, telefone):
    with closing(conectar_mysql()) as con, closing(con.cursor()) as cur:
        cur.execute("INSERT INTO clientes (nome, email, telefone) VALUES (%s, %s, %s)", [nome, email, telefone])
        id_aluno = cur.lastrowid
        con.commit()
        return id_aluno
    


db_criar_clientes("Leia", "leia@gmail.com", "11-994395999")