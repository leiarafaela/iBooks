from flask import Blueprint, make_response, render_template, redirect, request, session
import pickle
from controllers.homeController import carrinho
import mercadopago
import json

cart_bp = Blueprint('carrinho', __name__)
  
@cart_bp.route('/cart', methods=['GET'])
def cart():  
         
    produtos = carrinho
      
    return render_template('carrinho.html', carrinho=produtos)
   
@cart_bp.route('/criar_pagamento', methods=['POST'])
def criar_pagamento():
    total = 0
    for produto in carrinho:
        total += int(produto.preco)
     
    valorPagamento = total
      
    return redirect(payment(valorPagamento))
  
  
def payment(valorPagamento):
    valor =  int(valorPagamento)
    preference = { 
        "items": [
            {
                "title": "Pedido Ibooks",
                "description": "Pedido",
                "picture_url": "",
                "category_id": "orders",
                "quantity": 1,
                "currency_id": "BRL",
                "unit_price": valor
            }
        ]
    }

    mp = mercadopago.SDK("TEST-6749706992397515-032221-80c67714fe6c5cbc6c321d6122c6f65c-346350990")

    preferenceResult = mp.preference().create(preference)

    url = preferenceResult["response"]["init_point"]
    
    return url
 
def carregar_lista_do_cache(arquivo_cache):
    with open(arquivo_cache, 'rb') as arquivo:
        lista = pickle.load(arquivo)
    return lista
