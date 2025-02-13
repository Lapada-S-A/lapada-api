"""
Module for handling bid-related services, including creating bids.
"""

from db import db
from models.bid import Bid
from sqlalchemy import func


class BidService:
    """
    Service class for handling bid-related operations.
    """

    @staticmethod
    def create_bid(data):
        """
        Create a new bid.

        Args:
            data (dict): Data containing bid details.

        Returns:
            Bid: The created bid object.
        """
        auction_id = data['auction_id']
        amount = data['amount']

        highest_bid = db.session.query(func.max(Bid.amount)).filter_by(auction_id=auction_id).scalar()

        if highest_bid is not None and amount <= highest_bid:
            raise ValueError(f"O lance deve ser maior que {highest_bid:.2f}")

        bid = Bid(
            amount=data['amount'],
            auction_id=data['auction_id'],
            buyer_id=data['buyer_id']
        )

        db.session.add(bid)
        db.session.commit()

        return bid
