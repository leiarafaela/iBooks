from flask import Flask, make_response, jsonify, request
from model.Customer import Customer as customer

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False


@app.route('/')
def root():
    return "<h1>API de Clientes</h1>" 

@app.route('/clientes', methods=['GET'])
def get_all_customers():
    return make_response(jsonify(
        customer.getAll()))

@app.route('/clientes/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    return make_response(jsonify(
        customer.getById(customer_id)))

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
