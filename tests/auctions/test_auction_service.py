import pytest
from datetime import datetime
from app import app
from db import db
from models.auction import Auction
from services.auction_service import AuctionService
from models.status import Status


@pytest.fixture
def client():
    app = create_app()
    with app.test_client() as client:
        yield client


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
        db.session.commit()

    yield db

    with app.app_context():
        db.drop_all()

def test_create_auction(init_database):
    data = {
        "title": "Auction for Item XYZ",
        "end_date": "2024-12-21T10:00:00",
        "initial_value": 100.00,
        "min_increment": 5.00,
        "item_id": 1,
        "type_id": 1,
        "seller_id": 1,
        "status": "PENDING"
    }

    with app.app_context():
        auction_service = AuctionService()
        auction = auction_service.create_auction(data)

        assert auction.title == data["title"]
        assert auction.end_date == datetime.fromisoformat(data["end_date"])
        assert auction.initial_value == data["initial_value"]
        assert auction.status == Status.PENDING


def test_get_auction_by_id(init_database):
    with app.app_context():
        auction_service = AuctionService()
        auction = auction_service.get_auction_by_id(1)
        
        assert auction is not None
        assert auction.id == 1
        assert auction.title == "Auction Test"
