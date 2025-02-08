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
    def get_all_categories():
        """
        Retrieve all categories.

        Returns:
            list: List of all category objects.
        """
        return Category.query.all()
    
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
