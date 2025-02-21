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
        yield db
        db.session.remove()
        db.reflect()
        db.drop_all()

def test_create_auction_missing_fields(client, init_database):
    with app.app_context():
        data = {
            "title": "Test Auction"
        }
        response = client.post("/auction/create", json=data)
        assert response.status_code == 400
        assert "error" in response.json

def test_list_auctions(client, init_database):
    with app.app_context():
        response = client.get("/auction/list")
        assert response.status_code == 200
        assert isinstance(response.json, list)

def test_get_auction(client, init_database):
    with app.app_context():
        response = client.get("/auction/list/1")
        assert response.status_code in [200, 404]

def test_get_auction_not_found(client, init_database):
    with app.app_context():
        response = client.get("/auction/list/999")
        assert response.status_code == 404

def test_get_auctions_by_user_bids(client, init_database):
    with app.app_context():
        response = client.get("/auction/user/1")
        assert response.status_code == 200
