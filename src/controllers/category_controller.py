# pylint: disable=broad-except
"""
Category module endpoints for creating and listing categories.
"""
from flask import Blueprint, jsonify, request
from models.category import Category
from services.category_service import CategoryService

category_service = CategoryService()

category_bp = Blueprint('category', __name__, url_prefix='/category')


@category_bp.route('/create', methods=['POST'])
def create_category_endpoint():
    """
    Endpoint to create a new category.

    Request Body:
        {
            "name": "Electronics"
        }

    Returns:
        JSON response with the created category or error message.
    """
    data = request.get_json()

    if not data or 'name' not in data:
        return jsonify({'message': 'Invalid input, missing required fields'}), 400

    try:
        new_category = category_service.create_category(data)
        return jsonify(new_category.to_dict()), 201
    except Exception as e:
        return jsonify({'message': str(e)}), 400


@category_bp.route('/list', methods=['GET'])
def list_categories():
    """
    Endpoint to list all categories with pagination and ordering.

    Query Params:
        - page (int): Page number (default: None)
        - per_page (int): Items per page (default: None)
        - order_by (str): Field to order by ('id' or 'name')
        - order_asc (bool): If true, order ascending (default: false)
        - order_desc (bool): If true, order descending (default: false)

    Returns:
        JSON response with either a simple list or paginated categories.
    """
    try:
        page = request.args.get('page', type=int)
        per_page = request.args.get('per_page', type=int)
        order_by = request.args.get('order_by', default='id', type=str)
        order_asc = request.args.get('order_asc', default='false', type=str).lower() == 'true'
        order_desc = request.args.get('order_desc', default='false', type=str).lower() == 'true'

        categories = CategoryService.get_all_categories(page, per_page, order_by, order_asc, order_desc)

        if page is None or per_page is None:
            return jsonify([c.to_dict() for c in categories]), 200

        return jsonify({
            'categories': [c.to_dict() for c in categories.items],
            'total': categories.total,
            'page': categories.page,
            'per_page': categories.per_page,
            'pages': categories.pages
        }), 200

    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500




@category_bp.route('/list/<int:category_id>', methods=['GET'])
def get_category_by_id(category_id):
    """
    Endpoint to retrieve a category by ID.

    Returns:
        JSON response with the category details or an error message.
    """
    try:
        category_obj = category_service.get_category_by_id(category_id)
        if not category_obj:
            return jsonify({'message': 'Category not found'}), 404
        return jsonify(category_obj.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@category_bp.route('/update/<int:category_id>', methods=['PUT'])
def update_category(category_id):
    """
    Endpoint to update a category's details.

    Request Body:
        {
            "name": "Updated Category Name"
        }

    Returns:
        JSON response confirming update or an error message.
    """
    data = request.get_json()

    if not data or 'name' not in data:
        return jsonify({'message': 'Invalid input, missing required fields'}), 400

    try:
        result = category_service.update_category(category_id, data)
        if 'error' in result:
            return jsonify({'message': result['error']}), 404
        return jsonify({'category': result['category']}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 400


@category_bp.route('/delete/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    """
    Endpoint to delete a category only if it has no associated auctions.

    Returns:
        JSON response confirming deletion or an error message.
    """
    try:
        result = category_service.delete_category(category_id)
        if 'error' in result:
            return jsonify({'message': result['error']}), 400
        return jsonify({'message': 'Category deleted successfully'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 400
