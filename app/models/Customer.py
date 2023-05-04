from contextlib import closing
from model.Connection import conectar_mysql
from util import row_to_dict, rows_to_dict


class Customer():
    def getAll():
        with closing(conectar_mysql()) as con, closing(con.cursor()) as cur:
            cur.execute("SELECT * FROM clientes")
            return rows_to_dict(cur.description, cur.fetchall())

    def getById(id):
        with closing(conectar_mysql()) as con, closing(con.cursor()) as cur:
            cur.execute("SELECT * FROM clientes WHERE id= %s", [id])
            return row_to_dict(cur.description, cur.fetchone())

    def create(customer):
        with closing(conectar_mysql()) as con, closing(con.cursor()) as cur:
            cur.execute("INSERT INTO clientes (nome,email,cpf,celular,cidade,estado,bairro,numero,cep,complemento,logradouro,is_active) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", [
                customer['nome'], customer['email'], customer['cpf'], customer['celular'], customer['cidade'], customer['estado'], customer['bairro'], customer['numero'], customer['cep'], customer['complemento'], customer['logradouro'], 'False'])
            customer = cur.lastrowid
            con.commit()
            con.close()
            return customer

    def update(customer, id):
        with closing(conectar_mysql()) as con, closing(con.cursor()) as cur:
            cur.execute("UPDATE clientes SET nome = %s,email = %s,cpf = %s,celular = %s,cidade = %s,estado = %s,bairro = %s,numero = %s,cep = %s,complemento = %s,logradouro = %s WHERE id = %s", [
                customer['nome'], customer['email'], customer['cpf'], customer['celular'], customer['cidade'], customer['estado'], customer['bairro'], customer['numero'], customer['cep'], customer['complemento'], customer['logradouro'], id])
            con.commit()
            con.close()

    def delete(id):
        with closing(conectar_mysql()) as con, closing(con.cursor()) as cur:
            cur.execute("DELETE FROM clientes WHERE id = %s", [id])
            con.commit()
            con.close()
