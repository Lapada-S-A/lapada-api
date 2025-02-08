"""
Module for handling type-related services.
"""
from db import db
from models.type import Type


class TypeService:
    """
    Service class for handling type-related operations.
    """

    @staticmethod
    def create_type(data):
        """
        Create a new type.

        Args:
            data (dict): Data containing type details.

        Returns:
            Type: The created type object.
        """
        new_type = Type(
            name=data['name'],
            description=data['description']
        )

        db.session.add(new_type)
        db.session.commit()

        return new_type

    @staticmethod
    def get_all_types():
        """
        Retrieve all types.

        Returns:
            List[Type]: A list of all type objects.
        """
        return Type.query.all()

    @staticmethod
    def get_type_by_id(type_id):
        """
        Retrieve a type by ID.

        Args:
            type_id (int): The ID of the type.

        Returns:
            Type: The type object if found, otherwise None.
        """
        return Type.query.get(type_id)
