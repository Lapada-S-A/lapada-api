"""
Module for representing bids and their statuses in the database.
"""
import datetime

import pytest
from datetime import datetime
from app import app
from db import db

from models.bidstatus import BidStatus
from models.auction import Auction
from models.status import Status
from models.bid import Bid
from models.bidstatus import BidStatus
from models.type import Type

@pytest.fixture(scope='module')
def init_database():
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['TESTING'] = True

    with app.app_context():
        db.create_all()

        type_entry = Type(id=1, name="SomeType", description="SomeDescription")
        db.session.add(type_entry)
        db.session.commit()

        auction = Auction(
            title="Auction Test",
            description="Descrição para Auction Test",
            end_date=datetime(2024, 12, 21, 10, 0, 0),
            initial_value=100.00,
            min_increment=5.00,
            type_id=1,
            seller_id=1,
            status=Status.PENDING,
        )
        db.session.add(auction)

        bid_status_pending = BidStatus.ACTIVE

        bid = Bid(
            amount=50.00,
            auction_id=1,
            buyer_id=1,
            bid_status=bid_status_pending,
        )
        db.session.add(bid)

        db.session.commit()

        yield db

        db.session.remove()
        db.drop_all()

        db.drop_all()

def test_create_bid(init_database):
    with app.app_context():
        db = init_database
        bid = Bid.query.first()
        assert bid is not None
        assert bid.amount == 50.00
        assert bid.auction_id == 1
        assert bid.bid_status == BidStatus.ACTIVE

def test_list_bids_for_auction(init_database):
    with app.app_context():
        db = init_database
        auction = Auction.query.first()
        bids = Bid.query.filter_by(auction_id=auction.id).all()
        assert len(bids) > 0

def test_list_bids_with_limit(init_database):
    with app.app_context():
        db = init_database
        auction = Auction.query.first()
        limit = 1
        bids = Bid.query.filter_by(auction_id=auction.id).limit(limit).all()
        assert len(bids) == 1