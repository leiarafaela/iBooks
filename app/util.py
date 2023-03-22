import hashlib
import secrets



# Converte uma linha em um dicionário.
def row_to_dict(description, row):
    if row is None: return None
    d = {}
    for i in range(0, len(row)):
        d[description[i][0]] = row[i]
    return d

# Converte uma lista de linhas em um lista de dicionários.
def rows_to_dict(description, rows):
    result = []
    for row in rows:
        result.append(row_to_dict(description, row))
    return result


def criptografar_senha(senha):
    # gera um "salt" aleatório
    salt = secrets.token_hex(16)

    # concatena o "salt" à senha
    senha_com_salt = senha + salt

    # cria o hash da senha com o "salt" usando o algoritmo SHA256
    senha_criptografada = hashlib.sha256(senha_com_salt.encode()).hexdigest()

    return senha_criptografada, salt


def verificar_senha(senha, hash_armazenado, salt_armazenado):
    # concatena o "salt" à senha inserida
    senha_com_salt = senha + salt_armazenado

    # cria o hash da senha inserida com o "salt" usando o algoritmo SHA256
    senha_criptografada = hashlib.sha256(senha_com_salt.encode()).hexdigest()

    # compara o hash da senha inserida com o hash armazenado
    if senha_criptografada == hash_armazenado:
        return True
    else:
        return False
