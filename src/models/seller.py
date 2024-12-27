"""
Module for representing sellers in the database.
"""
from db import db


class Seller(db.Model):
    """
    Represents a seller entity in the database.

    Attributes:
        id (int): The primary key for the seller.
        name (str): The name of the seller (set to a fixed value for now).
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, default='Default Seller')
