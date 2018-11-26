from sqlalchemy.sql import func

from project import db


class Pdt(db.Model):

    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nomb = db.Column(db.String(50), nullable=False)
    cat = db.Column(db.String(50), nullable=False)
    cod = db.Column(db.String(20), nullable=False)
    stoc = db.Column(db.String(20), nullable=False)
    prec = db.Column(db.String(128), nullable=False)
    created_date = db.Column(db.DateTime, default=func.now(), nullable=False)

    def to_json(self):
        return {
            'id': self.id,
            'nomb': self.nomb,
            'cat': self.cat,
            'cod': self.cod,
            'stoc': self.stoc,
            'prec': self.prec
        }

    def __init__(self, nomb, cat, cod, stoc, prec):
        self.nomb = nomb
        self.cat = cat
        self.cod = cod
        self.stoc = stoc
        self.prec = prec
