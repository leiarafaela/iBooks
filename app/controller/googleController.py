import json
import os
import pathlib
from dotenv import load_dotenv

from flask import Blueprint, Flask, make_response, jsonify, render_template, url_for, redirect, request
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)

import requests
from model.Customer import Customer as customer
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
from oauthlib.oauth2 import WebApplicationClient
import google.auth.transport.requests

load_dotenv()
app = Flask(__name__, template_folder='../view/templates', static_folder='../view/static')
app.config['JSON_SORT_KEYS'] = False
app.secret_key = os.getenv('SECRET_KEY') or os.urandom(24)

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
GOOGLE_CLIENTE_ID = os.getenv('GOOGLE_CLIENT_ID')
GOOGLE_CLIENTE_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
GOOGLE_DISCOVERY_URL = ("https://accounts.google.com/.well-known/openid-configuration")

login_manager=LoginManager()
login_manager.init_app(app)

google_bp = Blueprint('google_bp', __name__)

@login_manager.unauthorized_handler
def unauthorized():
    return "Mensagemm de erro", 403

client=WebApplicationClient(GOOGLE_CLIENTE_ID)

@login_manager.user_loader
def load_user(customer_id):
    return jsonify(
        customer.getById(customer_id)) 

# @app.route('/')
# def index():
#     if current_user.is_authenticated:
#         return(
#             '<p>Voce está logado</p>'

#         )
#     return '<a class="button" href="/google"> Google login</a>'


@google_bp.route("/google")
def login_google():
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg['authorization_endpoint'] 

    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + '/callback',
        scope=['openid', 'email', 'profile']
    )
    return redirect(request_uri)

@google_bp.route('/google/callback')
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
    
    customernew = {'id': unique_id, 'nome': users_name, 'email': users_email, 'cpf': None, 'celular': None, 'cidade': None, 'estado': None, 'bairro': None, 'numero': None, 'cep': None, 'complemento': None, 'logradouro': None, 'is_active': False}   
    customer.create(customernew)

    login_user(customer)
    return redirect(url_for('index'))

def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json() 