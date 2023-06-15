import os
from flask import Blueprint, make_response, render_template, redirect, request, session
import pickle

home_bp = Blueprint('home_bp', __name__)

carrinho = []
 

 
@home_bp.route('/parceiros', methods=['GET'])
def parceiro():
    return render_template('cadastro-parceiro.html')

@home_bp.route('/cliente', methods=['GET'])
def cliente():
    return render_template('cadastro-cliente.html')

@home_bp.route('/paineladm', methods=['GET'])
def painelAdm():
    return render_template('painel-admin.html')




@home_bp.route('/adicionar', methods=['POST'])
def adicionar():
    produto_id = request.form['produto_id']
    valor = request.form['valor']
    
    produto = Produto(produto_id, valor)
    
    carrinho = CarrinhoDeCompras()
    
    carrinho.adicionar_produto(produto)
    
    carrinho.calcular_total()
         
    return redirect("/home")
  
    
@home_bp.route('/remover', methods=['POST'])
def remover():
    produto_id = request.form['id']
    
    produto = Produto(produto_id)
     
    carrinho.remover_produto(produto)
      
    carrinho.calcular_total()
      
    return redirect("/")
 
## Funcoes
class Produto:
    def __init__(self, nome, preco):
        self.nome = nome
        self.preco = preco

class CarrinhoDeCompras:
    def __init__(self):
        self.produtos = []

    def adicionar_produto(self, produto):
        self.produtos.append(produto)
        carrinho.append(produto)

    def remover_produto(self, produto):
        self.produtos.remove(produto)
        carrinho.remove(produto)

    def calcular_total(self):
        total = 0
        for produto in carrinho:
            total += float(produto.preco)
        session['total'] = total
        return total
    
    def retonar_lista():
        print(carrinho)
        return produtos


def salvar_lista_em_cache(lista, arquivo_cache):
    with open(arquivo_cache, 'wb') as arquivo:
        pickle.dump(lista, arquivo)
