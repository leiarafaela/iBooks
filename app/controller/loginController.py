import os
from dotenv import load_dotenv
from flask import Blueprint, Flask, make_response, jsonify, render_template, redirect, request
from model.Customer import Customer as customer
from controller.regras_negocio import create_costumer_login, login_check, create_parceiro_login
from integrations.twilio_call_OTP import verifica_otp, solicitar_otp

login_bp = Blueprint('login', __name__)

@login_bp.route('/', methods=['GET'])
def show_index():
    return make_response(redirect("/login"))
    #return render_template('login.html')

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

    if logado is False:
        error = 'Login invalido'
        return render_template("login.html", error=error)

    if logado is True: 
        solicitar_otp()
        return make_response(redirect("/otp")) #, render_template("otp.html")

@login_bp.route('/otp', methods=['GET'])
def show_otp():
    return render_template('otp.html')


@login_bp.route('/otp', methods=['POST'])
def verify_otp():
    error = None
    infos_auth = {}
    for chave, valor in request.form.items(): 
        infos_auth[chave] = valor
        
    retorno = verifica_otp(infos_auth['code'])
    
    if retorno is False:
        error = "Código inválido"
    else:
        return make_response(redirect("/menu"))