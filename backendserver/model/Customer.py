from contextlib import closing
from model.db_connection import conectar_mysql


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
        
    def update(id, customer):
        with closing(conectar_mysql()) as con, closing(con.cursor()) as cur:
            cur.execute("UPDATE clientes SET nome = %s, email = %s, telefone = %s WHERE id = %s", [customer['nome'], customer['email'], customer['telefone'], id])
            con.commit()
            con.close()
        
    def delete(id):
        with closing(conectar_mysql()) as con, closing(con.cursor()) as cur:
            cur.execute("DELETE FROM clientes WHERE id = %s", [id])
            con.commit()
            con.close()


            