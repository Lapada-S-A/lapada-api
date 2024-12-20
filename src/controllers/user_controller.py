from flask import Blueprint, request, jsonify
from services.user_service import add_user_type  # Assuming service functions are in user_service.py
from models import UserType

user_bp = Blueprint('user', __name__, url_prefix='/user')

@user_bp.route('/type', methods=['POST'])
def create_user_type():
    """
    Endpoint to create a new user type.

    Request Body:
        {
            "name": "buyer"
        }

    Returns:
        JSON response with the created user type.
    """
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({"error": "Invalid input"}), 400

    name = data['name']
    
    # Check if the user type already exists
    if UserType.query.filter_by(name=name).first():
        return jsonify({"error": "User type already exists"}), 400

    user_type = add_user_type(name)
    return jsonify(user_type.to_dict()), 201
