from db import db
from models.category import Category

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
    def get_all_categories(page=1, per_page=10, order_by='id', order='asc'):
        """
        Retrieve all categories with pagination and ordering.

        Args:
            page (int): Page number.
            per_page (int): Items per page.
            order_by (str): Field to order by ('id' or 'name').
            order (str): Order direction ('asc' or 'desc').

        Returns:
            Pagination object containing category objects.
        """
        valid_order_fields = ['id', 'name']
        valid_order_directions = ['asc', 'desc']
        
        if order_by not in valid_order_fields:
            order_by = 'id'
        if order not in valid_order_directions:
            order = 'asc'
        
        column = getattr(Category, order_by)
        if order == 'desc':
            column = column.desc()
        
        return Category.query.order_by(column).paginate(page=page, per_page=per_page, error_out=False)
    
    @staticmethod
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
