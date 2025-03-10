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
            jsonify({'message': 'Invalid input, missing required fields'}),
            400,
        )

    try:
        new_type = type_service.create_type(data)
        return jsonify(new_type.to_dict()), 201
    except Exception as e:
        return jsonify({'message': str(e)}), 400


@type_bp.route('/list', methods=['GET'])
def list_types():
    """
    Endpoint to list all types.

    Returns:
        JSON response with the list of types or an error message.
    """
    try:
        types = type_service.get_all_types()
        return jsonify([t.to_dict() for t in types]), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 400


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
            return jsonify({'message': 'Type not found'}), 404
        return jsonify(type_obj.to_dict()), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 400
