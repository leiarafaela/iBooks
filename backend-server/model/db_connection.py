import mysql.connector
from contextlib import closing
import os



def conectar_mysql():
    conn = mysql.connector.connect(
        user="b6a4da3f3869f6",
        password="dd33ced0",
        host="us-cdbr-east-06.cleardb.net",
        database="heroku_315c522990c1dd4"
    )

    return conn

def db_criar_clientes(nome, email, telefone):
    with closing(conectar_mysql()) as con, closing(con.cursor()) as cur:
        cur.execute("INSERT INTO clientes (nome, email, telefone) VALUES (%s, %s, %s)", [nome, email, telefone])
        id_aluno = cur.lastrowid
        con.commit()
        return id_aluno
    


db_criar_clientes("Gabriel", "gabriel@gmail.com", "11-99495999")