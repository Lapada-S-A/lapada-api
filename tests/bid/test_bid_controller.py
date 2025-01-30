import pytest
from app import app
from db import db
from models.bid import Bid, BidStatus
from models.auction import Auction
from models.status import Status
from datetime import datetime

@pytest.fixture
def client():
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

        bid_status_pending = BidStatus(id=1, name="Pending")
        db.session.add(bid_status_pending)

        db.session.commit()

    yield db

    with app.app_context():
        db.drop_all()


def test_create_bid(client, init_database):
    data = {
        "amount": 150.00,
        "auction_id": 1,
        "buyer_id": 2,
        "bid_status_id": 1
    }

    with app.app_context():
        response = client.post('/bid/create', json=data)
        assert response.status_code == 201
        json_data = response.get_json()
        assert json_data['amount'] == data['amount']
        assert json_data['auction_id'] == data['auction_id']
        assert json_data['buyer_id'] == data['buyer_id']
        assert json_data['bid_status_id'] == data['bid_status_id']


def test_create_bid_missing_fields(client, init_database):
    data = {
        "auction_id": 1,
        "buyer_id": 2,
        "bid_status_id": 1
    }

    with app.app_context():
        response = client.post('/bid/create', json=data)
        assert response.status_code == 400
        json_data = response.get_json()
        assert json_data['error'] == 'Invalid input, missing required fields'


def test_list_bids_for_auction(client, init_database):
    data = {
        "amount": 150.00,
        "auction_id": 1,
        "buyer_id": 2,
        "bid_status_id": 1
    }

    with app.app_context():
        client.post('/bid/create', json=data)

        response = client.get('/bid/list/1')
        assert response.status_code == 200
        json_data = response.get_json()
        assert isinstance(json_data, list)
        assert len(json_data) == 2
        assert json_data[0]['auction_id'] == 1


def test_list_bids_with_limit(client, init_database):
    data1 = {
        "amount": 150.00,
        "auction_id": 1,
        "buyer_id": 2,
        "bid_status_id": 1
    }
    data2 = {
        "amount": 200.00,
        "auction_id": 1,
        "buyer_id": 3,
        "bid_status_id": 1
    }

    with app.app_context():
        client.post('/bid/create', json=data1)
        client.post('/bid/create', json=data2)

        response = client.get('/bid/list/1?limit=1')
        assert response.status_code == 200
        json_data = response.get_json()
        assert len(json_data) == 1
        assert json_data[0]['amount'] == 200.00
