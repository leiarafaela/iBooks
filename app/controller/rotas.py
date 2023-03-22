from flask import Flask, make_response, jsonify, render_template, request
from model.Customer import Customer as customer
from model.Produtos import Produtos as produtos
from model.Parceiros import Parceiros as parceiro

app = Flask(__name__, template_folder='../view/templates')
app.config['JSON_SORT_KEYS'] = False

@app.route('/')
@app.route('/login')
def index():
    return render_template('login.html')

@app.route('/clientes', methods=['GET'])
def get_all_customers():
    return make_response(jsonify(
        customer.getAll()))

@app.route('/clientes/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    return jsonify(
        customer.getById(customer_id))

@app.route('/clientes', methods=['POST'])
def create_customer():
    body = request.json
    customer.create(body)
    return make_response(jsonify(
        message='Cliente cadastrado com sucesso.'))

@app.route('/clientes/<int:customer_id>', methods=['DELETE'])
def delete_customers(customer_id):
    customer.delete(customer_id)
    return make_response(jsonify(
        message='Cliente excluido com sucesso.'))

@app.route('/clientes/<int:customer_id>', methods=['PUT'])
def update(customer_id):
    body = request.json
    customer.update(customer_id, body)
    return make_response(jsonify(
        message='Cliente atualizado com sucesso.',
        customer=customer.getById(customer_id)))


    ############################################################################
    ##                                                                        ##
    ##                         ROTAS DE PRODUTOS                              ##
    ##                                                                        ##
    ############################################################################


@app.route('/produtos', methods=['GET'])
def get_all_products():
    return make_response(jsonify(
        produtos.getAll()))

@app.route('/produtos/<int:product_id>', methods=['GET'])
def get_products(product_id):
    return jsonify(
        produtos.getById(product_id))

@app.route('/produtos', methods=['POST'])
def create_products():
    body = request.json
    produtos.create(body)
    return make_response(jsonify(
        message='Produto cadastrado com sucesso.'))

@app.route('/produtos/<int:product_id>', methods=['DELETE'])
def delete_products(product_id):
    produtos.delete(product_id)
    return make_response(jsonify(
        message='Produto excluido com sucesso.'))

@app.route('/produtos/<int:product_id>', methods=['PUT'])
def update_products(product_id):
    body = request.json
    produtos.update(product_id, body)
    return make_response(jsonify(
        message='Produto atualizado com sucesso.',
        produtos=produtos.getById(product_id)))


    ############################################################################
    ##                                                                        ##
    ##                         ROTAS DE PARCEIROS                             ##
    ##                                                                        ##
    ############################################################################


@app.route('/parceiros', methods=['GET'])
def get_all_partners():
    return make_response(jsonify(
        parceiro.getAll()))

@app.route('/parceiros/<int:parceiro_id>', methods=['GET'])
def get_partner(parceiro_id):
    return jsonify(
        parceiro.getById(parceiro_id))

@app.route('/parceiros', methods=['POST'])
def create_partner():
    body = request.json
    parceiro.create(body)
    return make_response(jsonify(
        message='Parceiro cadastrado com sucesso.'))

@app.route('/parceiros/<int:parceiro_id>', methods=['DELETE'])
def delete_partners(parceiro_id):
    parceiro.delete(parceiro_id)
    return make_response(jsonify(
        message='Parceiro excluido com sucesso.'))

@app.route('/parceiros/<int:parceiro_id>', methods=['PUT'])
def update_partners(parceiro_id):
    body = request.json
    parceiro.update(parceiro_id, body)
    return make_response(jsonify(
        message='Parceiro atualizado com sucesso.',
        parceiro=parceiro.getById(parceiro_id)))
