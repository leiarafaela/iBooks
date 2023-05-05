from contextlib import closing
from models.Connection import conectar_mysql
from util import row_to_dict, rows_to_dict


class Produto():
    def getAll():
        with closing(conectar_mysql()) as con, closing(con.cursor()) as cur:
            cur.execute("SELECT * FROM produtos")
            return rows_to_dict(cur.description, cur.fetchall())
        
    
    def getById(id):
        with closing(conectar_mysql()) as con, closing(con.cursor()) as cur:
            cur.execute("SELECT * FROM produtos WHERE id = %s", [id])
            return row_to_dict(cur.description, cur.fetchone())
        
    def create(produtos):
        with closing(conectar_mysql()) as con, closing(con.cursor()) as cur:
            cur.execute("INSERT INTO produtos (nome, preco, sinopse, autor, editora, id_parceiro, quantidade) VALUES(%s,%s,%s,%s,%s,%s,%s)", [
                produtos['nome'], produtos['preco'], produtos['sinopse'], produtos['autor'],produtos['editora'], produtos['id_parceiro'], produtos['quantidade']])
            auth = cur.lastrowid
            con.commit()
            con.close()
            return auth
        
    def update(id, produtos):
        with closing(conectar_mysql()) as con, closing(con.cursor()) as cur:
                cur.execute("UPDATE produtos SET  name = %s, preco = %s, sinopse = %s, autor = %s, editora = %s, id_parceiro = %s, quantidade = %s WHERE id = %s", [
                            produtos['nome'], produtos['preco'], produtos['sinopse'], produtos['autor'],produtos['editora'], produtos['id_parceiro'], produtos['quantidade'],id])
                con.commit()
                con.close()

    def delete(id):
        with closing(conectar_mysql()) as con, closing(con.cursor()) as cur:
            cur.execute("DELETE FROM produtos WHERE id = %s", [id])
            con.commit()
            con.close()
