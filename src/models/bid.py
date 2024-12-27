"""
Module for representing bids and their statuses in the database.
"""
import datetime

from db import db


class Bid(db.Model):
    """
    Represents a bid entity in the database.

    Attributes:
        id (int): The primary key for the bid.
        amount (float): The amount of the bid.
        bid_date (datetime): The date when the bid was placed.
        auction_id (int): Foreign key referring to the auction.
        buyer_id (int): Foreign key referring to the buyer.
        bid_status_id (int): Foreign key referring to the bid status.
    """

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    bid_date = db.Column(
        db.DateTime, default=datetime.datetime.utcnow, nullable=False
    )
    auction_id = db.Column(
        db.Integer, db.ForeignKey('auction.id'), nullable=False
    )
    buyer_id = db.Column(
        db.Integer, nullable=False
    )  # FK com valor fixo do comprador
    bid_status_id = db.Column(
        db.Integer, nullable=False
    )  # FK para status do lance

    def to_dict(self):
        """
        Convert the Bid object into a dictionary.

        Returns:
            dict: A dictionary containing the Bid's attributes.
        """
        return {
            'id': self.id,
            'amount': self.amount,
            'bid_date': self.bid_date.isoformat(),
            'auction_id': self.auction_id,
            'buyer_id': self.buyer_id,
            'bid_status_id': self.bid_status_id,
        }


class BidStatus(db.Model):
    """
    Represents the status of a bid.

    Attributes:
        id (int): The primary key for the bid status.
        name (str): The name of the bid status.
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    def to_dict(self):
        """
        Convert the BidStatus object into a dictionary.

        Returns:
            dict: A dictionary containing the BidStatus's attributes.
        """
        return {'id': self.id, 'name': self.name}
