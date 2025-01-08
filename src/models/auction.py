"""
Module for representing and managing auctions in the database.import datetime
"""
import datetime

from db import db
from models.status import Status


class Auction(db.Model):
    """
    Represents an auction entity in the database.

    Attributes:
        id (int): The primary key for the auction.
        title (str): The title of the auction.
        created_date (datetime): The date when the auction was created.
        start_date (datetime): The starting date of the auction.
        end_date (datetime): The ending date of the auction.
        initial_value (float): The initial value of the auction.
        min_increment (float): The minimum increment value for buyers.
        item_id (int): Foreign key referring to the item.
        type_id (int): Foreign key referring to the type.
        buyer_id (int): Foreign key referring to the buyer.
        seller_id (int): Foreign key referring to the seller.
        status (Status): The status of the auction.
    """

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    created_date = db.Column(
        db.DateTime, default=datetime.datetime.utcnow, nullable=False
    )
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    initial_value = db.Column(db.Float, nullable=False)
    min_increment = db.Column(db.Float, nullable=False)
    item_id = db.Column(
        db.Integer, default=1, nullable=False
    )  # FK com valor fixo 1
    type_id = db.Column(
        db.Integer, default=1, nullable=False
    )  # FK com valor fixo 1
    buyer_id = db.Column(
        db.Integer, default=1, nullable=True
    )  # FK com valor fixo 1
    seller_id = db.Column(
        db.Integer, default=1, nullable=False
    )  # FK com valor fixo 1
    status = db.Column(db.Enum(Status), default=Status.PENDING, nullable=False)

    def to_dict(self):
        """
        Convert the Auction object into a dictionary.

        Returns:
            dict: A dictionary containing the Auction's attributes.
        """
        return {
            'id': self.id,
            'title': self.title,
            'created_date': self.created_date.isoformat(),
            'start_date': self.start_date.isoformat(),
            'end_date': self.end_date.isoformat(),
            'initial_value': self.initial_value,
            'min_increment': self.min_increment,
            'item_id': self.item_id,
            'type_id': self.type_id,
            'buyer_id': self.buyer_id,
            'seller_id': self.seller_id,
            'status': self.status.value,
        }
