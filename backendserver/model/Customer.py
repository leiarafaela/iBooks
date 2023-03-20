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
        database=database)
    return conn

class Customer():
    def getAll():
        with closing(conectar_mysql()) as con, closing(con.cursor()) as cur:
            cur.execute("SELECT * FROM clientes")
            return cur.fetchall()
        
    def getById(id):
        with closing(conectar_mysql()) as con, closing(con.cursor()) as cur:
            cur.execute("SELECT * FROM clientes WHERE id= %s", [id])
            return cur.fetchall()
          

    def create(customer):
        with closing(conectar_mysql()) as con, closing(con.cursor()) as cur:
            cur.execute("INSERT INTO clientes (nome, email, telefone) VALUES (%s, %s, %s)", [customer['nome'], customer['email'], customer['telefone']])
            customer = cur.lastrowid
            con.commit()
            con.close()
            return customer
        
    def delete(id):
        with closing(conectar_mysql()) as con, closing(con.cursor()) as cur:
            cur.execute("DELETE FROM clientes WHERE id = %s", [id])
            con.commit()
            con.close()

    def update(id, customer):
        with closing(conectar_mysql()) as con, closing(con.cursor()) as cur:
            cur.execute("UPDATE clientes SET nome = %s, email = %s, telefone = %s WHERE id = %s", [customer['nome'], customer['email'], customer['telefone'], id])
            con.commit()
            con.close()
            