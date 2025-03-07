from api import db
from passlib.hash import pbkdf2_sha256


class Usuario(db.Model):
    __tablename__ = "usuario"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    nome = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    senha = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean)
    api_key = db.Column(db.String(100), nullable=True)

    def encriptar_senha(self):
        self.senha = pbkdf2_sha256.hash(self.senha)

    def ver_senha(self, senha):
        return pbkdf2_sha256.verify(senha, self.senha)
