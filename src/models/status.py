from db import db

class Status(db.Model):
    """
    Represents a status entity in the database.

    Attributes:
        id (int): The primary key for the status.
        name (str): The status name.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)