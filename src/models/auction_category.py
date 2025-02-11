from db import db

auction_category = db.Table(
    '_AuctionCategories',
    db.Column('Auction_id', db.Integer, db.ForeignKey('Auction.id'), primary_key=True),
    db.Column('Category_id', db.Integer, db.ForeignKey('Category.id'), primary_key=True)
)