"""
Module for handling type-related services.
"""
from db import db
from models.auction import Auction
from models.type import Type
from sqlalchemy import asc, desc


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
    def get_all_types(page=None, per_page=None, order_by='id', order_asc=False, order_desc=False):
        """
        Retrieve categories with ordering, with optional pagination.

        Args:
            page (int, optional): Page number. If None, returns all results.
            per_page (int, optional): Number of items per page. If None, returns all results.
            order_by (str): Field to order by ('id' or 'name').
            order_asc (bool): Whether to sort in ascending order.
            order_desc (bool): Whether to sort in descending order.

        Returns:
            Pagination object if pagination is enabled, otherwise a list of Type objects.
        """
        if order_by not in ['id', 'name']:
            raise ValueError("Invalid order_by value. Use 'id' or 'name'.")

        if order_asc and order_desc:
            raise ValueError("Cannot set both order_asc and order_desc to true.")

        query = Type.query

        if order_asc:
            query = query.order_by(asc(getattr(Type, order_by)))
        elif order_desc:
            query = query.order_by(desc(getattr(Type, order_by)))
        else:
            query = query.order_by(asc(Type.id))  # Ordem padrão

        if page is None or per_page is None:
            return query.all()

        return query.paginate(page=page, per_page=per_page, error_out=False)

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
 
         associated_auctions = Auction.query.filter_by(type_id=type_id).first()
         if associated_auctions:
             return {'error': 'Cannot delete type. There are associated auctions.'}
 
         db.session.delete(type_obj)
         db.session.commit()
         return {'success': True}
