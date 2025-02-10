from db import db

auction_category = db.Table(
    'auction_category',
    db.Column('auction_id', db.Integer, db.ForeignKey('auction.id'), primary_key=True),
    db.Column('category_id', db.Integer, db.ForeignKey('category.id'), primary_key=True)
)