from db import db

auction_category = db.Table(
    'AuctionCategory',
    db.Column('auction_id', db.Integer, db.ForeignKey('Auction.id'), primary_key=True),
    db.Column('category_id', db.Integer, db.ForeignKey('Category.id'), primary_key=True)
)