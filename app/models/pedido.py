from datetime import datetime

from app import db


class Pedido(db.Model):

    __tablename__ = "pedidos"

    id = db.Column(db.Integer, primary_key=True)

    mesa_id = db.Column(
        db.Integer,
        db.ForeignKey("mesas.id"),
        nullable=False
    )

    status = db.Column(
        db.String(20),
        default="recebido"
    )

    total = db.Column(
        db.Float,
        default=0
    )

    criado_em = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    itens = db.relationship(
        "app.models.item_pedido.ItemPedido",
        backref="pedido",
        lazy=True,
        cascade="all, delete-orphan"
    )