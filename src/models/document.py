from datetime import datetime
from db import db

import base64
class Document(db.Model):
    __tablename__ = 'Document'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    pdfData = db.Column(db.LargeBinary, nullable=False)
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)
    clientId = db.Column(db.Integer, nullable=True)
    isIdentityDocument = db.Column(db.Boolean, default=True)

    auctionId = db.Column(db.Integer, db.ForeignKey('Auction.id'), nullable=True)
    auction = db.relationship('Auction', backref=db.backref('documents', lazy=True), lazy=True)


    def to_dict(self):
        return {
            "id": self.id,
            "auctionId": self.auctionId,
            "name": self.name,
            "pdfData": {
                "type": "Buffer",
                "data": list(self.pdfData) if self.pdfData else None  # Converte bytes para lista de inteiros
            },
            "createdAt": self.createdAt.isoformat() if self.createdAt else None
        }

