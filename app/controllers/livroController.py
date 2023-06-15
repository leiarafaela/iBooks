from flask import Blueprint, render_template


livro_bp = Blueprint('livro_bp', __name__)


@livro_bp.route('/livro/novo', methods=['GET'])
def show_livro_form():
    return render_template('cadastro-livro.html')