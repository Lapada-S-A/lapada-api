"""
Module for handling auction-related services
including creating and fetching auctions.
"""
from datetime import datetime

from db import db
from models.auction import Auction
from models.bid import Bid
from models.status import Status


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
        end_date = datetime.fromisoformat(data['end_date'])

        auction = Auction(
            title=data['title'],
            end_date=end_date,
            initial_value=data['initial_value'],
            min_increment=data['min_increment'],
            item_id=1,  # FK fixada para 1
            type_id=1,  # FK fixada para 1
            seller_id=1,  # FK fixada para 1
            status=data['status'],
            created_date=datetime.now()
        )

        db.session.add(auction)
        db.session.commit()

        return auction

    @staticmethod
    def get_all_auctions(page=1, per_page=10, filters=None):
        """
        Fetch paginated auctions with optional filters.

        Args:
            page (int): Page number for pagination.
            per_page (int): Number of items per page.
            filters (dict): Optional filters for query.

        Returns:
            Pagination object with filtered auctions.
        """
        query = Auction.query

        if filters:
            if 'title' in filters:
                query = query.filter(Auction.title == filters['title'])
            if 'category_id' in filters:
                query = query.filter(Auction.category_id == filters['category_id'])
            if 'type_id' in filters:
                query = query.filter(Auction.type_id == filters['type_id'])
            if 'status' in filters:
                query = query.filter(Auction.status == filters['status'])
            if 'min_bid' in filters:
                query = query.filter(Auction.current_bid >= filters['min_bid'])
            if 'max_bid' in filters:
                query = query.filter(Auction.current_bid <= filters['max_bid'])
            if 'end_date' in filters:
                query = query.filter(Auction.end_date == filters['end_date'])

        return query.paginate(page=page, per_page=per_page, error_out=False)

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

    @staticmethod
    def get_auctions_by_user_bids(user_id, page, per_page):
        """
            Fetches auctions in which a user has placed bids.

            Args:
                user_id (int): The ID of the user.
                page (int): Page number.
                per_page (int): Number of items per page.

            Returns:
                Pagination: Paginated list of auctions.
        """

        auctions = (
            db.session.query(Auction)
            .join(Bid)
            .filter(Bid.buyer_id == user_id)
            .distinct()
            .paginate(page=page, per_page=per_page, error_out=False)
        )
        return auctions
    
    
    @staticmethod
    def update_auction_status(auction, new_status, expected_status=None):
        """
        Update the status of an auction.

        Args:
            auction (Auction): The auction object to update.
            new_status (Status): The new status to set.
            expected_status (Status): The expected status of the auction.

        Returns:
            Auction: The updated auction object.
        """
        if expected_status and auction.status != expected_status:
            raise ValueError(f'Auction must be {expected_status.name.lower()} to change status.')
        if expected_status  == Status.FINISHED and auction.end_date < datetime.now():
            raise ValueError('End date has not been reached yet.')
        auction.status = new_status
        db.session.commit()
        return auction

    @staticmethod
    def get_highest_bid(auction_id):
        """
        Fetch the highest bid for a given auction.

        Args:
            auction_id (int): The ID of the auction to fetch the highest bid for.

        Returns:
            float: The highest bid amount.
        """
        highest_bid = db.session.query(Bid.amount).filter(Bid.auction_id == auction_id).order_by(Bid.amount.desc()).first()
        return highest_bid[0] if highest_bid else None
