"""
Module for representing types in the database.
"""
from db import db


class Type(db.Model):
    """
    Represents a type entity in the database.

    Attributes:
        id (int): The primary key for the type.
        name (str): The name of the type.
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
