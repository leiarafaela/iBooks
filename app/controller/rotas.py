
import os
from dotenv import load_dotenv
from flask import Flask, make_response, jsonify, render_template, redirect, request

from model.Customer import Customer as customer
from model.Produtos import Produtos as produtos
from model.Parceiros import Parceiros as parceiro
from controller.regras_negocio import create_costumer_login, login_check, create_parceiro_login
from OTPverification.basics_OTP import verifica_otp, solicitar_otp


load_dotenv()
app = Flask(__name__, template_folder='../view/templates', static_folder='../view/static')
app.config['JSON_SORT_KEYS'] = False
app.secret_key = os.getenv('SECRET_KEY') or os.urandom(24)


################ VISUALIZAÇÃO FORM E LOGIN ##########################
@app.route('/', methods=['GET'])
def show_index():
    return make_response(redirect("/login"))
    #return render_template('login.html')

@app.route('/login', methods=['GET'])
def show_login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    error = None
    infos_auth = {}
    for chave, valor in request.form.items():
        if chave == "email" and valor == "":
            error = "Informar email"
            return render_template("login.html", error=error)
            
        if chave == "senha" and valor == "":
            error = "Informar senha"
            return render_template("login.html", error=error)
            
        infos_auth[chave] = valor
        
    logado = login_check(infos_auth)

    if logado is False:
        error = 'Login invalido'
        return render_template("login.html", error=error)

    if logado is True: 
        solicitar_otp()
        return make_response(redirect("/otp")) #, render_template("otp.html")

##############################################################################
##                                                                          ##
##                              OTP                                         ##
##                                                                          ##
##############################################################################

@app.route('/otp', methods=['GET'])
def show_otp():
    return render_template('otp.html')


@app.route('/otp', methods=['POST'])
def verify_otp():
    error = None
    infos_auth = {}
    for chave, valor in request.form.items(): 
        infos_auth[chave] = valor
        
    retorno = verifica_otp(infos_auth['code'])
    
    if retorno is False:
        error = "Código inválido"
        return render_template("otp.html", error=error)
    else:
        return make_response(redirect("/menu"))
    
##############################################################################
##                                                                          ##
##                              MENU                                        ##
##                                                                          ##
##                                                                          ##
##############################################################################
@app.route('/menu', methods=['GET'])
def show_menu():
    return render_template('menu.html')


##############################################################################
##                                                                          ##
##                              CRUD CLIENTES                               ##
##                                                                          ##
##                                                                          ##
##############################################################################
@app.route('/clientes', methods=['GET'])
def get_all_customers():
    list_customer = customer.getAll()

    return render_template("painel-admin.html", usuarios=list_customer)

@app.route('/clientes/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    return jsonify(
        customer.getById(customer_id))


##################### VISUALIZAÇÃO FORM E CRIAÇÃO CLIENTE ##########################
@app.route('/cliente/novo', methods=['GET'])
def show_customer_form():
    return render_template('cadastro-cliente.html')

@app.route('/cliente/novo', methods=['POST'])
def create_customer():
    infos_custumer = {}
    infos_auth = {}
    for chave, valor in request.form.items():
        if chave == "senha" or chave == "email":
            infos_auth[chave] = valor
            
        infos_auth['tipo_acesso'] = 1
        
        infos_custumer[chave] = valor

    infos_auth['tipo_acesso'] = 1
    newCustomer = create_costumer_login(infos_custumer, infos_auth)


    message = f"O usuario {newCustomer} foi criado com sucesso."

    return render_template('menu.html', message=message)

@app.route('/delete/<int:customer_id>', methods= ['GET','DELETE'])
def delete_customers(customer_id):
    cliente=customer.getById(customer_id)
    if cliente is not None:
        customer.delete(customer_id)
    return render_template('menu.html')



@app.route('/atualizar/<int:customer_id>', methods=['GET'])
def show_update(customer_id):
    cliente=customer.getById(customer_id)
    return render_template('update-cliente.html', cliente=cliente)


@app.route('/atualizar/<int:customer_id>', methods=['POST'])
def update(customer_id):
    infos_customer = {}
    infos_auth = {}
    infos_customer['id'] = customer_id
    for chave, valor in request.form.items():
        if chave == "email":
            infos_auth[chave] = valor

        infos_customer[chave] = valor


    updateCustomer = customer.update(infos_customer, customer_id)


    message = f"O usuario {updateCustomer} foi atualizado com sucesso."

    return render_template('menu.html', message=message)


##############################################################################
##                                                                           ##
##                              CRUD PARCEIROS                               ##
##                                                                           ##
##############################################################################

@app.route('/parceiro/novo', methods=['GET'])
def show_parceiro_form():
    return render_template('cadastro-parceiro.html')


@app.route('/parceiro/novo', methods=['POST'])
def create_parceiro():
    infos_parceiro = {}
    infos_auth = {}
    for chave, valor in request.form.items():
        if chave == "senha" or chave == "email":
            infos_auth[chave] = valor
            
        infos_auth['tipo_acesso'] = 1
        
        infos_parceiro[chave] = valor

    infos_auth['tipo_acesso'] = 1
    newParceiro = create_parceiro_login(infos_parceiro, infos_auth)


    message = f"Empresa {newParceiro} foi criado com sucesso."

    return render_template('menu.html', message=message)