import pytest
from datetime import datetime
from app import app
from db import db
from models.bid import Bid, BidStatus
from models.auction import Auction
from models.status import Status
from services.bid_service import BidService

@pytest.fixture(scope='module')
def init_database():
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['TESTING'] = True

    with app.app_context():
        db.create_all()

        auction = Auction(
            title="Auction Test",
            end_date=datetime(2024, 12, 21, 10, 0, 0),
            initial_value=100.00,
            min_increment=5.00,
            item_id=1,
            type_id=1,
            seller_id=1,
            status=Status.PENDING,
        )
        db.session.add(auction)

        bid_status_pending = BidStatus(id=1, name="Pending")
        db.session.add(bid_status_pending)

        db.session.commit()

    yield db

    with app.app_context():
        db.drop_all()


def test_create_bid_service(init_database):
    data = {
        "amount": 150.00,
        "auction_id": 1,
        "buyer_id": 2,
        "bid_status_id": 1
    }

    with app.app_context():
        bid_service = BidService()
        bid = bid_service.create_bid(data)

        assert bid.amount == data['amount']
        assert bid.auction_id == data['auction_id']
        assert bid.buyer_id == data['buyer_id']
        assert bid.bid_status_id == data['bid_status_id']


def test_create_bid_service_missing_fields(init_database):
    data = {
        "auction_id": 1,
        "buyer_id": 2,
        "bid_status_id": 1
    }

    with app.app_context():
        bid_service = BidService()
        with pytest.raises(KeyError):
            bid_service.create_bid(data)