"""
Module for handling auction-related services
including creating and fetching auctions.
"""
from datetime import datetime

from db import db
from models.auction import Auction


class AuctionService:
    """
    Service class for handling auction-related operations.
    """

    @staticmethod
    def create_auction(data):
        """
        Create a new auction with fixed foreign keys set to 1.

        Args:
            data (dict): Data containing auction details.

        Returns:
            Auction: The created auction object.
        """
        start_date = datetime.fromisoformat(data['start_date'])
        end_date = datetime.fromisoformat(data['end_date'])

        auction = Auction(
            title=data['title'],
            start_date=start_date,
            end_date=end_date,
            initial_value=data['initial_value'],
            min_increment=data['min_increment'],
            item_id=1,  # FK fixada para 1
            type_id=1,  # FK fixada para 1
            buyer_id=1,
            seller_id=1,  # FK fixada para 1
            status_id=1,  # FK fixada para 1
        )

        db.session.add(auction)
        db.session.commit()

        return auction

    @staticmethod
    def get_all_auctions(page, per_page):
        """
        Fetches all auctions with pagination.

        Args:
            page (int): The page number.
            per_page (int): The number of items per page.

        Returns:
            Pagination: The paginated result of auctions.
        """
        return Auction.query.paginate(
            page=page, per_page=per_page, error_out=False
        )

    @staticmethod
    def get_auction_by_id(auction_id):
        """
        Fetches an auction by its ID from the database.

        Args:
            auction_id (int): The ID of the auction to fetch.

        Returns:
            Auction: The Auction object if found, else None.
        """
        return Auction.query.get(auction_id)

    @staticmethod
    def get_auctions_by_status(status_id, page, per_page):
        """
        Fetches auctions that match the given status_id with pagination.

        Args:
            status_id (int): The status ID to filter auctions by.
            page (int): The page number.
            per_page (int): The number of items per page.

        Returns:
            Pagination: The paginated result of auctions.
        """
        return Auction.query.filter_by(status_id=status_id).paginate(
            page=page, per_page=per_page, error_out=False
        )
