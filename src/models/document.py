from datetime import datetime
from db import db

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
