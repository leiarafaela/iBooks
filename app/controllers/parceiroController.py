import os
from dotenv import load_dotenv
from flask import Blueprint, Flask, make_response, jsonify, render_template, redirect, request
from controllers.regras_negocio import create_parceiro_login
from models.Parceiro import Parceiro as parceiro

parceiro_bp = Blueprint('parceiro_bp', __name__)

@parceiro_bp.route('/parceiro/novo', methods=['GET'])
def show_parceiro_form():
    return render_template('cadastro-parceiro.html')


@parceiro_bp.route('/parceiro/novo', methods=['POST'])
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