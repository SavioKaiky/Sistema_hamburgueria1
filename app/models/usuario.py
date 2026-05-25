from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class Usuario(db.Model):

    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)

    nome = db.Column(db.String(100), nullable=False)

    usuario = db.Column(db.String(50), unique=True, nullable=False)

    senha = db.Column(db.String(255), nullable=False)

    permissao = db.Column(db.String(20), nullable=False)

    def set_senha(self, senha):
        self.senha = generate_password_hash(senha)

    def verificar_senha(self, senha):
        return check_password_hash(self.senha, senha)