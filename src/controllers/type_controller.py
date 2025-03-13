# pylint: disable=broad-except
"""
Type module endpoints for creating and listing types.
"""
from flask import Blueprint, jsonify, request
from models.type import Type
from services.type_service import TypeService

type_service = TypeService()

type_bp = Blueprint('type', __name__, url_prefix='/type')


@type_bp.route('/create', methods=['POST'])
def create_type_endpoint():
    """
    Endpoint to create a new type.

    Request Body:
        {
            "name": "Electronics",
            "description": "Electronic devices and gadgets"
        }

    Returns:
        JSON response with the created type or error message.
    """
    data = request.get_json()

    required_fields = ['name', 'description']
    if not data or not all(field in data for field in required_fields):
        return (
            jsonify({'error': 'Invalid input, missing required fields'}),
            400,
        )

    try:
        new_type = type_service.create_type(data)
        return jsonify(new_type.to_dict()), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@type_bp.route('/list', methods=['GET'])
def list_types():
    """
    Endpoint to list all types with pagination and ordering.

    Query Params:
        - page (int): Page number (default: 1)
        - per_page (int): Items per page (default: 10)
        - order_by (str): Field to order by ('id' or 'name')
        - order_asc (bool): If true, order ascending (default: false)
        - order_desc (bool): If true, order descending (default: false)

    Returns:
        JSON response with paginated list of types.
    """
    try:
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=10, type=int)
        order_by = request.args.get('order_by', default='id', type=str)
        order_asc = request.args.get('order_asc', default='false', type=str).lower() == 'true'
        order_desc = request.args.get('order_desc', default='false', type=str).lower() == 'true'

        types_pagination = TypeService.get_all_types(page, per_page, order_by, order_asc, order_desc)

        return jsonify({
            'types': [c.to_dict() for c in types_pagination.items],
            'total': types_pagination.total,
            'page': types_pagination.page,
            'per_page': types_pagination.per_page,
            'pages': types_pagination.pages
        }), 200

    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@type_bp.route('/list/<int:type_id>', methods=['GET'])
def get_type_by_id(type_id):
    """
    Endpoint to retrieve a type by ID.

    Returns:
        JSON response with the type details or an error message.
    """
    try:
        type_obj = type_service.get_type_by_id(type_id)
        if not type_obj:
            return jsonify({'error': 'Type not found'}), 404
        return jsonify(type_obj.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

    
@type_bp.route('/update/<int:type_id>', methods=['PUT'])
def update_type(type_id):
     """
     Endpoint to update an existing type.
 
     Request Body:
         {
             "name": "Updated Name",
             "description": "Updated Description"
         }
 
     Returns:
         JSON response with the updated type or an error message.
     """
     data = request.get_json()
 
     if not data:
         return jsonify({'error': 'No data provided'}), 400
 
     try:
         updated_type = type_service.update_type(type_id, data)
         if not updated_type:
             return jsonify({'error': 'Type not found'}), 404
         return jsonify(updated_type.to_dict()), 200
     except Exception as e:
         return jsonify({'error': str(e)}), 400
 
 
@type_bp.route('/delete/<int:type_id>', methods=['DELETE'])
def delete_type(type_id):
     """
     Endpoint to delete a type.
 
     Returns:
         JSON response confirming deletion or an error message.
     """
     try:
         result = type_service.delete_type(type_id)
         if 'error' in result:
             return jsonify({'error': result['error']}), 400
         return jsonify({'message': 'Type deleted successfully'}), 200
     except Exception as e:
         return jsonify({'error': str(e)}), 400
