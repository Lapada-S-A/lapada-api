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
from models.bidstatus import BidStatus
from models.document import Document

from services.bid_service import BidService


class AuctionService:
    """
    Service class for handling auction-related operations.
    """

    @staticmethod
    def create_auction(data, photos):
        """
        Create a new auction with fixed foreign keys set to 1.

        Args:
            data (dict): Data containing auction details.

        Returns:
            Auction: The created auction object.
        """
        end_date = datetime.fromisoformat(data['end_date'])
        created_date = datetime.now()

        AuctionService._validate_auction_dates(created_date, end_date)

        auction = Auction(
            title=data['title'],
            end_date=end_date,
            initial_value=data['initial_value'],
            min_increment=data['min_increment'],
            description=data['description'],
            seller_id=data['seller_id'],
            status=data['status'],
            type_id=data['type_id'],
            created_date=created_date
        )
        categories = Category.query.filter(Category.id.in_(data.get('categories', []))).all()
        if not categories:
            raise ValueError("Nenhuma categoria válida encontrada")
        if len(categories) != len(data.get('categories', [])):
            raise ValueError("Alguma categoria não foi encontrada")
        
        auction.categories = categories

        db.session.add(auction)
        db.session.commit()

        documents = []
        for _, photo in photos.items():
            if photo:
                document = Document(
                    name=photo.filename,
                    pdfData=photo.read(),
                    auctionId=auction.id,
                    isIdentityDocument=False,
                    clientId=None
                )
                documents.append(document)

        print(f"Auction ID: {auction.id}")
        for document in documents:
            print(f"Document Name: {document.name}, Auction ID: {document.auctionId}")
            db.session.add(document)

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

        if page is not None and per_page is not None:
            return query.paginate(page=page, per_page=per_page, error_out=False)
        return query.all()


    @staticmethod
    def get_auction_by_id(auction_id):
        """
        Fetches an auction by its ID from the database.

        Args:
            auction_id (int): The ID of the auction to fetch.

        Returns:
            Auction: The Auction object if found, else None.
        """
        auction = Auction.query.get(auction_id)
        documents = Document.query.filter_by(auctionId=auction_id).all()

        if not auction:
            return None

        return {
            "auction": auction,
            "documents": documents
        }
    
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
            raise ValueError(f'Leilão deve ser {expected_status.name.lower()} pra mudar status.')
        if expected_status  == Status.FINISHED and auction.end_date < datetime.now():
            raise ValueError('Data final ainda não chegou')
        auction.status = new_status
        db.session.commit()
        return auction

    @staticmethod
    def cancel_auction(auction_id):
        """
        Cancela um leilão, definindo o status para CANCELED e os lances como CANCELED.
        """
        auction = AuctionService.get_auction_by_id(auction_id)
        if not auction:
            raise ValueError("Leilão não encontrado")
        
        if auction.status != Status.ACTIVE:
            raise ValueError("Somente leilões ativos podem ser cancelados.")

        bids = Bid.query.filter(Bid.auction_id == auction_id).all()
        bid_ids = [bid.id for bid in bids]
        print(bid_ids)
        
        BidService.update_bid_statuses(bid_ids, BidStatus.CANCELED)

        auction.status = Status.CANCELED
        db.session.add(auction)

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Erro ao salvar alterações no banco: {e}")
        return auction

    @staticmethod
    def finish_auction(auction_id):
        """
        Finaliza um leilão, definindo o status para FINISHED e o maior lance como WINNER.
        """
        auction = AuctionService.get_auction_by_id(auction_id)
        if not auction:
            raise ValueError("Leilão não encontrado")
        
        if auction.status != Status.ACTIVE:
            raise ValueError("Somente leilões ativos podem ser finalizados.")

        highest_bid = (
            db.session.query(Bid)
            .filter(Bid.auction_id == auction_id)
            .order_by(Bid.amount.desc())
            .first()
        )

        if highest_bid:
            BidService.update_bid_statuses([highest_bid.id], BidStatus.WINNER)

        auction.status = Status.FINISHED
        db.session.add(auction)

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Erro ao salvar alterações no banco: {e}")
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
    
    @staticmethod
    def update_auction(auction_id, data):
        try:
            auction = Auction.query.get(auction_id)
            if not auction:
                raise ValueError("Leilão não encontrado")

            if 'title' in data:
                auction.title = data['title']
            if 'description' in data:
                auction.description = data['description']
            if 'end_date' in data:
                try:
                    auction.end_date = datetime.fromisoformat(data['end_date'])
                    AuctionService._validate_auction_dates(auction.created_date, auction.end_date)
                except ValueError:
                    raise ValueError("Formato de data inválida")
            if 'initial_value' in data:
                auction.initial_value = data['initial_value']
            if 'min_increment' in data:
                auction.min_increment = data['min_increment']
            if "categories" in data:
                category_ids = data["categories"]
                auction.categories = Category.query.filter(Category.id.in_(category_ids)).all()
                
                if len(auction.categories) != len(category_ids):
                    raise ValueError("Uma ou mais categorias informadas não existem.")

            db.session.commit()
            return auction

        except (ValueError) as e:
            db.session.rollback()
            raise Exception(f"Erro ao atualizar leilão: {str(e)}")


    @staticmethod
    def get_auctions_by_seller(seller_id):
        """
        Retrieve all auctions for a specific seller.

        Args:
            seller_id (int): The seller's ID.

        Returns:
            list: A list of dictionaries containing auction details.
        """
        auctions = Auction.query.filter_by(seller_id=seller_id).all()
        
        return [auction.to_dict() for auction in auctions]

    @staticmethod
    def _validate_auction_dates(created_date, end_date):
        if end_date < datetime.utcnow():
            raise ValueError("A data de término não pode ser anterior ao dia de hoje.")
        if created_date > end_date:
            raise ValueError("A data de criação não pode ser posterior à data de término.")


    @staticmethod
    def get_auctions_by_categories_and_status(categories_ids, status, page=None, per_page=None):
        """
        Fetch auctions filtered by category IDs and status (e.g., PENDING).

        Args:
            categories_ids (list): List of category IDs to filter auctions.
            status (Status): The status of the auctions (e.g., Status.PENDING).
            page (int, optional): Page number for pagination.
            per_page (int, optional): Number of items per page.

        Returns:
            Pagination or List: Paginated auctions or all auctions if no pagination.
        """
        query = Auction.query.filter(
            Auction.status == status,
            Auction.categories.any(Category.id.in_(categories_ids))
        )

        if page is not None and per_page is not None:
            return query.paginate(page=page, per_page=per_page, error_out=False)
        return query.all()