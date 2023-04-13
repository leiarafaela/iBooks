from model.Customer import Customer 
from model.Produto import Produto
from model.Parceiro import Parceiro
from model.Auth import Auth
from util import criptografar_senha, verificar_senha
from integrations.pyrebase import CreateAuthenticationByFirebase, SendResetPassword, AuthenticationByFirebase 


def  create_costumer_login(costumer, auth):
    create_custumer = Customer.create(costumer)
    email = auth['email']
    senha = auth['senha']
    userFirebase =  CreateAuthenticationByFirebase(email, senha)
    crip, salt = criptografar_senha(auth['senha'])
    auth['senha'] = crip
    auth['salt'] = salt
    Auth.create(auth)
    
    return create_custumer


def update_customer(costumer, auth):
    existEmail = Auth.getByEmail(auth['email'])

    if existEmail is None:
            email = auth['email']
            senha = auth['senha']
            userFirebase =  CreateAuthenticationByFirebase(email, senha)
            crip, salt = criptografar_senha(auth['senha'])
            auth['senha'] = crip
            auth['salt'] = salt
            Auth.create(auth)
    else:
        if existEmail['email'] != auth['email']:
            Auth.delete(existEmail['id'])
            crip, salt = criptografar_senha(auth['senha'])
            auth['senha'] = crip
            auth['salt'] = salt
            Auth.create(auth)
    
    update_customer = Customer.update(costumer)
    return update_customer


def login_check(auth):
    check = Auth.getByEmail(auth['email']) 
    if check is True:
            email = auth['email']
            senha = auth['senha']
        try:
            userFirebase = AuthenticationByFirebase(email, senha)
        except:
         return False
    return False

  



def create_parceiro_login(parceiro, auth):
    create_parceiro = Parceiro.create(parceiro)
    crip, salt = criptografar_senha(auth['senha'])
    auth['senha'] = crip
    auth['salt'] = salt
    Auth.create(auth)
    
    return create_parceiro
