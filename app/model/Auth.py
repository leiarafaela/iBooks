from contextlib import closing
from model.Connection import conectar_mysql
from util import row_to_dict, rows_to_dict



class Auth():
    def getAll():
        with closing(conectar_mysql()) as con, closing(con.cursor()) as cur:
            cur.execute("SELECT * FROM login_users")
            return rows_to_dict(cur.description, cur.fetchall())
        
    
    def getById(id):
        with closing(conectar_mysql()) as con, closing(con.cursor()) as cur:
            cur.execute("SELECT * FROM login_users WHERE id = %s", [id])
            return row_to_dict(cur.description, cur.fetchone())
        
    def create(auth):
        with closing(conectar_mysql()) as con, closing(con.cursor()) as cur:
            cur.execute("INSERT INTO login_users (email, senha, tipo_acesso, salt) VALUES(%s,%s,%s,%s)", [
                auth['email'], auth['senha'], auth['tipo_acesso'], auth['salt']])
            auth = cur.lastrowid
            con.commit()
            con.close()
            return auth
        
    def update(id, auth):
        with closing(conectar_mysql()) as con, closing(con.cursor()) as cur:
                cur.execute("UPDATE login_users SET email=%s, senha=%s, tipo_acesso=%s, salt=%s WHERE id = %s", [
                            auth['email'], auth['senha'], auth['tipo_acesso'], auth['salt'],id])
                con.commit()
                con.close()

    def delete(id):
        with closing(conectar_mysql()) as con, closing(con.cursor()) as cur:
            cur.execute("DELETE FROM login_users WHERE id = %s", [id])
            con.commit()
            con.close()
