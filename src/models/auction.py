from db import db
import datetime

class Auction(db.Model):
    """
    Represents a leilao entity in the database.

    Attributes:
        id (int): The primary key for the leilao.
        title (str): The title of the leilao.
        created_date (datetime): The date when the leilao was created.
        start_date (datetime): The starting date of the leilao.
        end_date (datetime): The ending date of the leilao.
        initial_value (float): The initial value of the leilao.
        min_increment (float): The minimum increment value for buyers.
        item_id (int): Foreign key referring to the item.
        type_id (int): Foreign key referring to the type.
        buyer_id (int): Foreign key referring to the buyer.
        seller_id (int): Foreign key referring to the seller.
        status_id (int): Foreign key referring to the status.
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    initial_value = db.Column(db.Float, nullable=False)
    min_increment = db.Column(db.Float, nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    type_id = db.Column(db.Integer, db.ForeignKey('type.id'), nullable=False)
    buyer_id = db.Column(db.Integer, db.ForeignKey('buyer.id'), nullable=True)
    seller_id = db.Column(db.Integer, db.ForeignKey('seller.id'), nullable=False)
    status_id = db.Column(db.Integer, db.ForeignKey('status.id'), nullable=False)
