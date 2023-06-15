import os
from flask import Flask
from controllers.loginController import login_bp
from controllers.customerController import cliente_bp
from controllers.googleController import google_bp
from controllers.livroController import livro_bp
from controllers.homeController import home_bp
from controllers.carrinhoController import cart_bp


app = Flask(__name__, template_folder='views/templates', static_folder='views/static')
app.config['JSON_SORT_KEYS'] = False
app.secret_key = os.getenv('SECRET_KEY') or os.urandom(24)

app.register_blueprint(login_bp)
app.register_blueprint(google_bp)
app.register_blueprint(cliente_bp)
app.register_blueprint(livro_bp)
app.register_blueprint(home_bp)
app.register_blueprint(cart_bp)



if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)
    