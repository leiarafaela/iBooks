import os
from flask import Flask
from controller.loginController import login_bp
from controller.customerController import cliente_bp

app = Flask(__name__, template_folder='view/templates', static_folder='view/static')
app.config['JSON_SORT_KEYS'] = False
app.secret_key = os.getenv('SECRET_KEY') or os.urandom(24)

app.register_blueprint(login_bp)
app.register_blueprint(cliente_bp)


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)