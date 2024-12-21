"""
Module for handling bid-related services, including creating bids.
"""

from db import db
from models.bid import Bid


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
        bid = Bid(
            amount=data['amount'],
            auction_id=data['auction_id'],
            buyer_id=data['buyer_id'],
            bid_status_id=data['bid_status_id'],
        )

        db.session.add(bid)
        db.session.commit()

        return bid
