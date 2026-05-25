from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():

    app = Flask(__name__)

    app.config.from_object("config.Config")

    db.init_app(app)

    from app.routes.auth import auth
    from app.routes.route import route
    from app.models.usuario import Usuario
    from app.models.mesa import Mesa
    from app.models.pedido import Pedido
    from app.models.item_pedido import ItemPedido

    app.register_blueprint(auth)
    app.register_blueprint(route)

    return app