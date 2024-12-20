from db import db
from datetime import datetime

class UserType(db.Model):
    """
    Represents a type of user in the database.

    Attributes:
        id (int): The primary key for the user type.
        name (str): The name of the user type (e.g., buyer, seller, curator, administrator).
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)

    def to_dict(self):
        """
        Convert the UserType object into a dictionary.

        Returns:
            dict: A dictionary containing the UserType's attributes.
        """
        return {
            'id': self.id,
            'name': self.name
        }

class User(db.Model):
    """
    Represents a buyer entity in the database.

    Attributes:
        id (int): The primary key for the buyer.
        name (str): The name of the buyer.
        age (int): The age of the buyer.
        email (str): The email address of the buyer.
        password (str): The password for the buyer (not hashed for now).
        cpf (str): The CPF (Cadastro de Pessoas Físicas) of the buyer.
        created_at (datetime): The datetime when the buyer was created.
        is_seller (bool): Whether the buyer is also a seller.
        phone_number (str): The phone number of the buyer.
        type_user_id (int): The foreign key referencing the UserType table.
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)  # Sem hash no momento
    cpf = db.Column(db.String(14), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    is_seller = db.Column(db.Boolean, default=False, nullable=False)
    phone_number = db.Column(db.String(15), nullable=True)
    type_user_id = db.Column(db.Integer, db.ForeignKey('user_type.id'), nullable=False)

    type_user = db.relationship('UserType', backref=db.backref('users', lazy=True))

    def to_dict(self):
        """
        Convert the Buyer object into a dictionary.

        Returns:
            dict: A dictionary containing the Buyer's attributes.
        """
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'email': self.email,
            'cpf': self.cpf,
            'created_at': self.created_at.isoformat(),
            'is_seller': self.is_seller,
            'phone_number': self.phone_number,
            'type_user': self.type_user.to_dict() if self.type_user else None
        }
