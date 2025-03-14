from datetime import datetime
from db import db

class Review(db.Model):
    __tablename__ = 'Review'

    id = db.Column(db.Integer, primary_key=True)
    rate = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    buyer_id = db.Column(db.Integer, nullable=False)
    seller_id = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        """Converte o objeto para dicionário (para JSON)."""
        return {
            "id": self.id,
            "rate": self.rate,
            "comment": self.comment,
            "created_at": self.created_at.strftime('%d-%m-%Y-%H-%M-%S'),
            "updated_at": self.updated_at.strftime('%d-%m-%Y-%H-%M-%S'),
            "buyer_id": self.buyer_id,
            "seller_id": self.seller_id,
        }