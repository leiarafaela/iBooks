from flask import Blueprint, jsonify, make_response, redirect, render_template, request
from controllers.regras_negocio import create_costumer_login
from models.Customer import Customer as customer
from models.Livro import Livro as livro

cliente_bp = Blueprint('cliente_bp', __name__)

@cliente_bp.route('/admin', methods=['GET'])
def get_all_customers_ibooks():
    list_customer = customer.getAll()
    list_ibooks = livro.getAll() 

    return render_template("painel-admin.html", usuarios=list_customer, livros=list_ibooks)

@cliente_bp.route('/clientes/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    return jsonify(
        customer.getById(customer_id))


##################### VISUALIZAÇÃO FORM E CRIAÇÃO CLIENTE ##########################
@cliente_bp.route('/cliente/novo', methods=['GET'])
def show_customer_form():
    return render_template('cadastro-cliente.html')

@cliente_bp.route('/cliente/novo', methods=['POST'])
def create_customer():
    infos_customer = {}
    infos_auth = {}
    for chave, valor in request.form.items():
        if chave == "senha" or chave == "email":
            infos_auth[chave] = valor
            
        infos_auth['tipo_acesso'] = 1
        
        infos_customer[chave] = valor

    infos_auth['tipo_acesso'] = 1
    newCustomer = create_costumer_login(infos_customer, infos_auth)

    message = f"O usuario {newCustomer} foi criado com sucesso."

    return make_response(redirect("/login"))

@cliente_bp.route('/delete/<int:customer_id>', methods= ['GET','DELETE'])
def delete_customer(customer_id):
    cliente=customer.getById(customer_id)
    if cliente is not None:
        customer.delete(customer_id)
    return make_response(redirect('/admin'))


@cliente_bp.route('/atualizar/<int:customer_id>', methods=['GET'])
def show_update(customer_id):
    cliente=customer.getById(customer_id)
    return render_template('update-cliente.html', cliente=cliente)


@cliente_bp.route('/atualizar/<int:customer_id>', methods=['POST'])
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

    return render_template('painel-admin.html', message=message)
