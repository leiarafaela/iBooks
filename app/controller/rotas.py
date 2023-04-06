import json
import os
import pathlib
from dotenv import load_dotenv

from flask import Flask, make_response, jsonify, render_template, url_for, redirect, request
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
import requests
from model.Customer import Customer as customer
from model.Produtos import Produtos as produtos
from model.Parceiros import Parceiros as parceiro
from controller.regras_negocio import create_costumer_login, login_check, update_customer, create_parceiro_login
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
from oauthlib.oauth2 import WebApplicationClient
import google.auth.transport.requests


load_dotenv()
app = Flask(__name__, template_folder='../view/templates', static_folder='../view/static')
app.config['JSON_SORT_KEYS'] = False
app.secret_key = os.getenv('SECRET_KEY') or os.urandom(24)

################## GOOGLE #####################
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
GOOGLE_CLIENTE_ID = os.getenv('GOOGLE_CLIENT_ID')
GOOGLE_CLIENTE_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
GOOGLE_DISCOVERY_URL = ("https://accounts.google.com/.well-known/openid-configuration")

login_manager=LoginManager()
login_manager.init_app(app)

@login_manager.unauthorized_handler
def unauthorized():
    return "Mensagemm de erro", 403

client=WebApplicationClient(GOOGLE_CLIENTE_ID)

@login_manager.user_loader
def load_user(customer_id):
    return jsonify(
        customer.getById(customer_id)) 

@app.route('/')
def index():
    if current_user.is_authenticated:
        return(
            '<p>Voce está logado</p>'

        )
    return '<a class="button" href="/google"> Google login</a>'


@app.route("/google")
def login_google():
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg['authorization_endpoint'] 

    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + '/callback',
        scope=['openid', 'email', 'profile']
    )
    return redirect(request_uri)

@app.route('/google/callback')
def callback():
    code = request.args.get('code')

    google_provider_cfg = get_google_provider_cfg()

    token_endpoint =google_provider_cfg['token_endpoint']
    token_url,headers,body = client.prepare_token_request(
        token_endpoint,
        authorization_responst=request.url,
        redirect_url=request.base_url,
        code=code
)
    token_response=requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENTE_ID, GOOGLE_CLIENTE_SECRET),
    )

    client.parse_request_body_response(json.dumps(token_response.json()))

    userinfo_endpoint= google_provider_cfg['userinfo_endpoint']
    uri,headers,body= client.add_token(userinfo_endpoint)
    userinfo_response= requests.get(uri,headers=headers, data=body)
    print(userinfo_response.json())

    if userinfo_response.json().get('email_verified'):
        unique_id= userinfo_response.json()['sub']
        users_email= userinfo_response.json()['email']
        picture=userinfo_response.json()['picture']
        users_name=userinfo_response.json()['given_name']
    else:
        return "Email de usuário indisponível ou não verificado pelo Google", 400
    
    customernew= {'id': unique_id, 'nome': users_name, 'email': users_email, 'cpf': None, 'celular': None, 'cidade': None, 'estado': None, 'bairro': None, 'numero': None, 'cep': None, 'complemento': None, 'logradouro': None}   
    customer.create(customernew)

    login_user(customer)
    return redirect(url_for('index'))



def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()    


################## HOME #####################



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