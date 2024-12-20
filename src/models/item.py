from datetime import datetime
from db import db


class Item(db.Model):
    """
    Represents an item entity in the database.

    Attributes:
        id (int): The primary key for the item.
        name (str): The name of the item.
        description (str): A brief description of the item.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(200), nullable=False)