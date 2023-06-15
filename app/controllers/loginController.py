import os
from flask import Blueprint, make_response, render_template, redirect, request
from models.Livro import Livro 
from controllers.regras_negocio import create_costumer_login, login_check, create_parceiro_login
from integrations.twilio_call_OTP import verifica_otp, solicitar_otp

login_bp = Blueprint('login', __name__)

@login_bp.route('/', methods=['GET'])
@login_bp.route('/login', methods=['GET'])
def show_login():
    return render_template('login.html')

@login_bp.route('/login', methods=['POST'])
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

    if logado:
        # clienteCel = customer.getCelByEmail(infos_auth['email'])
        solicitar_otp()
        return make_response(redirect("/otp"))
    else: 
        error = 'Login inválido'
        return render_template("login.html", error=error)

@login_bp.route('/otp', methods=['GET'])
def show_otp():
    return render_template('otp.html')


@login_bp.route('/otp', methods=['POST'])
def verify_otp():
    infos_auth = {}
    for chave, valor in request.form.items(): 
        infos_auth[chave] = valor
        
    retorno = verifica_otp(infos_auth['code'])
    
    if retorno:
        return make_response(redirect("/home", ))
    else:
        return render_template('otp.html', erro='Código inválido!')
    
@login_bp.route('/home', methods=['GET'])
def show_home():
    livros= Livro.getAll()
    return render_template('home.html', livros=livros)

@login_bp.route('/reset', methods=['GET'])
def show_reset():
    return render_template('reset-password.html')