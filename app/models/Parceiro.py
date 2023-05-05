from contextlib import closing
from models.Connection import conectar_mysql
from util import row_to_dict, rows_to_dict

class Parceiro():
    def getAll():
        with closing(conectar_mysql()) as con, closing(con.cursor()) as cur:
            cur.execute("SELECT * FROM parceiros")
            return rows_to_dict(cur.description, cur.fetchall())

    def getById(id):
        with closing(conectar_mysql()) as con, closing(con.cursor()) as cur:
            cur.execute("SELECT * FROM parceiros WHERE id= %s", [id])
            return row_to_dict(cur.description, cur.fetchone())

    def create(parceiro):
        with closing(conectar_mysql()) as con, closing(con.cursor()) as cur:
            cur.execute("INSERT INTO parceiros (nome_empresa, cnpj, celular, email, cidade, estado, bairro, cep, numero, complemento, lougradouro) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s %s, %s)", [
                        parceiro['nome_empresa'], parceiro['cnpj'], parceiro['celular'], parceiro['email'], parceiro['cidade'], parceiro['estado'],
                        parceiro['bairro'], parceiro['cep'], parceiro['numero'], parceiro['complemento'], parceiro['lougradouro']])
            parceiro = cur.lastrowid
            con.commit()
            con.close()
            return parceiro

    def update(id, parceiro):
        with closing(conectar_mysql()) as con, closing(con.cursor()) as cur:
            cur.execute("UPDATE parceiros SET nome_empresa = %s, cnpj = %s, celular = %s, email = %s, cidade = %s, estado = %s, bairro = %s, cep = %s, numero = %s,"+
                        " complemento = %s,lougradouro = %s WHERE id = %s", [
                        parceiro['nome_empresa'], parceiro['cnpj'], parceiro['celular'], parceiro['email'], parceiro['cidade'], parceiro['estado'],
                        parceiro['bairro'], parceiro['cep'], parceiro['numero'], parceiro['complemento'], parceiro['lougradouro'], id])
            con.commit()
            con.close()

    def delete(id):
        with closing(conectar_mysql()) as con, closing(con.cursor()) as cur:
            cur.execute("DELETE FROM parceiros WHERE id = %s", [id])
            con.commit()
            con.close()
