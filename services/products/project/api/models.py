from sqlalchemy.sql import func

from project import db


class Product(db.Model):

    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(50), nullable=False)
    categoria = db.Column(db.String(50), nullable=False)
    codigo = db.Column(db.String(20), nullable=False)
    stock = db.Column(db.String(20), nullable=False)
    precio = db.Column(db.String(128), nullable=False)
    created_date = db.Column(db.DateTime, default=func.now(), nullable=False)

    def to_json(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'categoria': self.categoria,
            'codigo': self.codigo,
            'stock': self.stock,
            'precio': self.precio
        }

    def __init__(self, nombre, categoria, codigo, stock, precio):
        self.nombre = nombre
        self.categoria = categoria
        self.codigo = codigo
        self.stock = stock
        self.precio = precio
