"""
Module for handling bid-related services, including creating bids.
"""

from db import db
from models.bid import Bid, BidStatus
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

        highest_bid = db.session.query(Bid).filter_by(auction_id=auction_id)\
                                       .order_by(Bid.amount.desc())\
                                       .first()

        if highest_bid is not None and amount <= highest_bid.amount:
            raise ValueError(f"O lance deve ser maior que {highest_bid.amount:.2f}")

        # highest_bid.bid_status = BidStatus.EXPIRED
        # db.session.add(highest_bid)
        db.session.query(Bid).filter_by(auction_id=auction_id).update({"bid_status": BidStatus.EXPIRED})

        bid = Bid(
            amount=data['amount'],
            auction_id=data['auction_id'],
            buyer_id=data['buyer_id']
        )

        db.session.add(bid)
        db.session.commit()

        return bid
    
    @staticmethod
    def get_bids_by_buyer_in_auction(auction_id: int, buyer_id: int, page: int = 1, per_page: int = 10):
        """
        Busca todos os lances de um comprador em um leilão específico.

        Args:
            auction_id (int): ID do leilão.
            buyer_id (int): ID do comprador.
            page (int): Página atual para paginação.
            per_page (int): Número de itens por página.

        Returns:
            Pagination: Objeto de paginação contendo os lances.
        """
        return Bid.query.filter_by(auction_id=auction_id, buyer_id=buyer_id)\
                        .order_by(Bid.bid_date.desc())\
                        .paginate(page=page, per_page=per_page, error_out=False)
    
    @staticmethod
    def update_bid_statuses(bid_ids, status):
        """
        Atualiza o status de múltiplos lances de uma vez, economizando consultas.
        """
        db.session.query(Bid).filter(Bid.id.in_(bid_ids)).update({Bid.bid_status: status}, synchronize_session=False)
        db.session.commit()
