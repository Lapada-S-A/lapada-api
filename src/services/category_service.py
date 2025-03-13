from db import db
from models.category import Category
from sqlalchemy import asc, desc

class CategoryService:
    """
    Service class for handling category-related operations.
    """
    
    @staticmethod
    def create_category(data):
        """
        Create a new category.

        Args:
            data (dict): Data containing category details.

        Returns:
            Category: The created category object.
        """
        category = Category(
            name=data['name']
        )
        
        db.session.add(category)
        db.session.commit()
        
        return category
    
    @staticmethod
    def get_all_categories(page, per_page, order_by, order_asc, order_desc):
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

        query = Category.query

        if order_asc:
            query = query.order_by(asc(getattr(Category, order_by)))
        elif order_desc:
            query = query.order_by(desc(getattr(Category, order_by)))
        else:
            query = query.order_by(asc(Category.id))  # Ordem padrão

        if page is None or per_page is None:
            return query.all()

        return query.paginate(page=page, per_page=per_page, error_out=False)

    def get_category_by_id(category_id):
        """
        Retrieve a category by its ID.

        Args:
            category_id (int): The ID of the category.

        Returns:
            Category: The category object if found, else None.
        """
        return Category.query.get(category_id)

    @staticmethod
    def update_category(category_id, data):
        """
        Update a category's details.

        Args:
            category_id (int): The ID of the category to update.
            data (dict): Dictionary containing updated category details.

        Returns:
            dict: {'success': True} if updated, {'error': 'message'} if not found.
        """
        category = Category.query.get(category_id)
        if not category:
            return {'error': 'Category not found'}

        if 'name' in data:
            category.name = data['name']

        db.session.commit()
        return {'success': True, 'category': category.to_dict()}

    @staticmethod
    def delete_category(category_id):
        """
        Delete a category only if it has no associated auctions.

        Args:
            category_id (int): The ID of the category.

        Returns:
            dict: {'success': True} if deleted, {'error': 'message'} if not found or has dependencies.
        """
        category = Category.query.get(category_id)
        if not category:
            return {'error': 'Category not found'}

        # Verifica se há leilões associados
        if category.auctions:
            return {'error': 'Cannot delete category. There are associated auctions.'}

        db.session.delete(category)
        db.session.commit()
        return {'success': True}
