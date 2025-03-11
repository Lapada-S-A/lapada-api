"""
Module for handling type-related services.
"""
from db import db
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
    def get_all_types(page, per_page, order_by, order_asc, order_desc):
        """
        Retrieve paginated categories with ordering.

        Args:
            page (int): Page number.
            per_page (int): Number of items per page.
            order_by (str): Field to order by ('id' or 'name').
            order_asc (bool): Whether to sort in ascending order.
            order_desc (bool): Whether to sort in descending order.

        Returns:
            Pagination object with categories.
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
