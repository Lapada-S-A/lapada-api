"""
Module for handling type-related services.
"""
from db import db
from models.type import Type

from models.auction import Auction


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

    @staticmethod
    def update_type(type_id, data):
        """
        Update an existing type.

        Args:
            type_id (int): The ID of the type to update.
            data (dict): Data containing updated fields.

        Returns:
            Type: The updated type object if found, otherwise None.
        """
        type_obj = Type.query.get(type_id)
        if not type_obj:
            return None

        if 'name' in data:
            type_obj.name = data['name']
        if 'description' in data:
            type_obj.description = data['description']

        db.session.commit()
        return type_obj

    @staticmethod
    def delete_type(type_id):
        """
        Delete a type by ID only if it has no associated auctions.

        Args:
            type_id (int): The ID of the type.

        Returns:
            dict: {'success': True} if deleted, {'error': 'message'} if not found or has dependencies.
        """
        type_obj = Type.query.get(type_id)
        if not type_obj:
            return {'error': 'Type not found'}

        # Verifica se existem leilões associados a esse tipo
        associated_auctions = Auction.query.filter_by(type_id=type_id).first()
        if associated_auctions:
            return {'error': 'Cannot delete type. There are associated auctions.'}

        db.session.delete(type_obj)
        db.session.commit()
        return {'success': True}
