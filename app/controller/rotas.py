from flask import Flask, make_response, jsonify, render_template, request, url_for, redirect
from model.Customer import Customer as customer
from model.Produtos import Produtos as produtos
from model.Parceiros import Parceiros as parceiro
from controller.regras_negocio import create_costumer_login, login_check, update_customer, create_parceiro_login

app = Flask(__name__, template_folder='../view/templates')
app.config['JSON_SORT_KEYS'] = False


################## HOME #####################
@app.route('/')
@app.route('/home')
def home():
    return render_template('menu.html')


################ VISUALIZAÇÃO FORM E LOGIN ##########################
@app.route('/login', methods=['GET'])
def show_login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    infos_auth = {}
    for chave, valor in request.form.items():
        infos_auth[chave] = valor

    logado = login_check(infos_auth)

    if not logado:
        return render_template("/login.html", erro="ERRO")
    
    return render_template("menu.html",  mensagem = "")
    


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