from app import db

class Mesa(db.Model):

    __tablename__ = "mesas"

    id = db.Column(db.Integer, primary_key=True)

    numero = db.Column(db.Integer, unique=True, nullable=False)

    status = db.Column(db.String(20), default="livre")

    pedidos = db.relationship(
        "app.models.pedido.Pedido",
        backref="mesa",
        lazy=True
    )