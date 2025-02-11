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
        description (str): A description of the type.
    """
    __tablename__ = 'Type'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(300), nullable=False)

    def to_dict(self):
        """
        Convert the Type object into a dictionary.

        Returns:
            dict: A dictionary containing the Type's attributes.
        """
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
        }
