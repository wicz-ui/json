from flask import Flask

from config import SECRET_KEY
from rotas_auth import registrar_rotas_auth
from rotas_clientes import registrar_rotas_clientes
from rotas_produtos import registrar_rotas_produtos


app = Flask(__name__)
app.secret_key = SECRET_KEY


registrar_rotas_auth(app)
registrar_rotas_clientes(app)
registrar_rotas_produtos(app)


if __name__ == '__main__':
    app.run(debug=True)
