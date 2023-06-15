from contextlib import closing
from models.Connection import conectar_mysql
from util import row_to_dict, rows_to_dict


class Livro():
    def getAll():
        with closing(conectar_mysql()) as con, closing(con.cursor()) as cur:
            cur.execute("SELECT * FROM livros")
            return rows_to_dict(cur.description, cur.fetchall())
        
    
    def getById(id):
        with closing(conectar_mysql()) as con, closing(con.cursor()) as cur:
            cur.execute("SELECT * FROM livros WHERE id = %s", [id])
            return row_to_dict(cur.description, cur.fetchone())
        
    def create(livro): 
        with closing(conectar_mysql()) as con, closing(con.cursor()) as cur:
            cur.execute("INSERT INTO livros (nome, preco, qtd_estoque) VALUES(%s,%s,%s)", [
                livro['nome'], livro['preco'], livro['qtd_estoque'], ])
            livro = cur.lastrowid
            con.commit()
            con.close()
            return livro
        
    def update(id, produtos):
        with closing(conectar_mysql()) as con, closing(con.cursor()) as cur:
                cur.execute("UPDATE livros SET  name = %s, preco = %s, sinopse = %s, autor = %s, editora = %s, id_parceiro = %s, quantidade = %s WHERE id = %s", [
                            produtos['nome'], produtos['preco'], produtos['sinopse'], produtos['autor'],produtos['editora'], produtos['id_parceiro'], produtos['quantidade'],id])
                con.commit()
                con.close()

    def delete(id):
        with closing(conectar_mysql()) as con, closing(con.cursor()) as cur:
            cur.execute("DELETE FROM livros WHERE id = %s", [id])
            con.commit()
            con.close()
