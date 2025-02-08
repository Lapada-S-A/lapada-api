"""
Module for representing categorys in the database.
"""
from db import db


class Category(db.Model):
    """
    Represents a category entity in the database.

    Attributes:
        id (int): The primary key for the category.
        name (str): The name of the category.
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    def to_dict(self):
        """
        Convert the Category object into a dictionary.

        Returns:
            dict: A dictionary containing the Category's attributes.
        """
        return {
            'id': self.id,
            'name': self.name
        }
