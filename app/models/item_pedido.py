from app import db


class ItemPedido(db.Model):

    __tablename__ = "itens_pedido"

    id = db.Column(db.Integer, primary_key=True)

    pedido_id = db.Column(
        db.Integer,
        db.ForeignKey("pedidos.id"),
        nullable=False
    )

    nome = db.Column(
        db.String(100),
        nullable=False
    )
    

    preco = db.Column(
        db.Float,
        nullable=False
    )

    quantidade = db.Column(
        db.Integer,
        default=1
    )