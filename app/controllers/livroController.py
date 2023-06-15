import os
from flask import Blueprint, make_response, redirect, render_template, request
from models.Livro import Livro 


livro_bp = Blueprint('livro_bp', __name__)


@livro_bp.route('/livro/novo', methods=['GET'])
def show_ibook_register():
    return render_template('cadastro-livro.html')


@livro_bp.route('/livro/novo', methods=['POST'])
def create_ibook():
    infos_livro = {}
    for chave, valor in request.form.items():
        infos_livro[chave] = valor

    if 'img' in request.files:
        imagem = request.files['img']

        imagem.save('app/views/static/img/' + infos_livro['nome'] + '.jpg')

    newIbook = Livro.create(infos_livro)

    message = f"O usuario {newIbook} foi criado com sucesso."

    return make_response(redirect("/admin"))

@livro_bp.route('/delete/livro/<int:ibook_id>', methods= ['GET','DELETE'])
def delete_ibook(ibook_id):
    livro= Livro.getById(ibook_id)
    if livro:
        Livro.delete(ibook_id)
    return make_response(redirect('/admin'))