"""
Module for handling auction-related services
including creating and fetching auctions.
"""
from datetime import datetime
from random import randint

from sqlalchemy import func

from db import db
from models.auction import Auction
from models.bid import Bid
from models.status import Status
from models.category import Category


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
            description=data['description'],  # FK fixada para 1
            seller_id=1,  # FK fixada para 1
            status=data['status'],
            type_id=data['type_id'],
            created_date=datetime.now()
        )

        db.session.add(auction)
        db.session.commit()

        return auction

    @staticmethod
    def get_all_auctions(page=None, per_page=None, filters=None):
        """
        Fetch auctions with optional pagination and filters.

        Args:
            page (int, optional): Page number for pagination.
            per_page (int, optional): Number of items per page.
            filters (dict, optional): Optional filters for query.

        Returns:
            List or pagination object with filtered auctions.
        """
        query = Auction.query

        if filters:
            if 'title' in filters:
                query = query.filter(Auction.title == filters['title'])
            if 'description' in filters:
                query = query.filter(Auction.description == filters['description'])
            if 'type_id' in filters:
                query = query.filter(Auction.type_id == filters['type_id'])
            if 'status' in filters:
                query = query.filter(Auction.status == filters['status'])
            if 'end_date' in filters:
                try:
                    end_date = datetime.strptime(filters['end_date'], "%Y-%m-%d").date()
                    query = query.filter(func.date(Auction.end_date) <= end_date)
                except ValueError:
                    raise ValueError("Formato de data inválido. Use 'YYYY-MM-DD'.")

            if 'min_bid' in filters or 'max_bid' in filters:
                highest_bids = (
                    db.session.query(
                        Bid.auction_id, 
                        func.max(Bid.amount).label("highest_bid")
                    )
                    .group_by(Bid.auction_id)
                    .subquery()
                )
                query = query.join(highest_bids, Auction.id == highest_bids.c.auction_id)

                if 'min_bid' in filters:
                    query = query.filter(highest_bids.c.highest_bid >= filters['min_bid'])
                if 'max_bid' in filters:
                    query = query.filter(highest_bids.c.highest_bid <= filters['max_bid'])

        # Se page e per_page forem passados, retorna com paginação, senão retorna lista normal
        if page is not None and per_page is not None:
            return query.paginate(page=page, per_page=per_page, error_out=False)
        return query.all()


    @staticmethod
    def get_auction_by_id(auction_id):
        """
        Fetches an auction by its ID from the database, including item details.

        Args:
            auction_id (int): The ID of the auction to fetch.

        Returns:
            dict: A dictionary containing auction and item details.
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
    
    def add_categories_to_auction(self, auction_id, category_ids):
        """
        Associa múltiplas categorias a um leilão.
        """
        auction = Auction.query.get(auction_id)
        if not auction:
            raise ValueError("Leilão não encontrado")

        categories = Category.query.filter(Category.id.in_(category_ids)).all()
        if not categories:
            raise ValueError("Nenhuma categoria válida encontrada")

        auction.categories = categories
        db.session.commit()