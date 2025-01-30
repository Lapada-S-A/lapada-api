import pytest
from datetime import datetime
from app import app
from db import db
from models.status import Status
from models.auction import Auction
from services.auction_service import AuctionService


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
        db.session.commit()

    yield db

    with app.app_context():
        db.drop_all()


def test_create_auction(client, init_database):
    data = {
        "title": "Auction for Item XYZ",
        "end_date": "2024-12-21T10:00:00",
        "initial_value": 100.00,
        "min_increment": 5.00,
        "item_id": 1,
        "type_id": 1,
        "seller_id": 1
    }

    with app.app_context():
        response = client.post('/auction/create', json=data)
        assert response.status_code == 201
        json_data = response.get_json()
        assert json_data['title'] == data['title']
        assert json_data['end_date'] == data['end_date']
        assert json_data['status'] == 'PENDING'


def test_create_auction_missing_fields(client, init_database):
    data = {
        "end_date": "2024-12-21T10:00:00",
        "initial_value": 100.00,
        "min_increment": 5.00,
        "item_id": 1,
        "type_id": 1,
        "seller_id": 1
    }

    with app.app_context():
        response = client.post('/auction/create', json=data)
        assert response.status_code == 400
        json_data = response.get_json()
        assert json_data['error'] == 'Invalid input, missing required fields'


def test_list_auctions(client, init_database):
    with app.app_context():
        response = client.get('/auction/list')
        assert response.status_code == 200
        json_data = response.get_json()
        assert isinstance(json_data, list)
        assert len(json_data) > 0


def test_get_auction(client, init_database):
    with app.app_context():
        response = client.get('/auction/list/1')
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data['title'] == "Auction Test"
        assert json_data['id'] == 1


def test_get_auction_not_found(client, init_database):
    with app.app_context():
        response = client.get('/auction/list/9999')
        assert response.status_code == 404
        json_data = response.get_json()
        assert json_data['error'] == 'Auction not found'


def test_get_auctions_by_user_bids(client, init_database):
    with app.app_context():
        response = client.get('/auction/user/1')
        assert response.status_code == 200
        json_data = response.get_json()
        assert isinstance(json_data, list)


def test_internal_server_error(client):
    with app.app_context():
        response = client.get('/auction/list_by_status/1000')
        assert response.status_code == 500
        json_data = response.get_json()
        assert 'error' in json_data
