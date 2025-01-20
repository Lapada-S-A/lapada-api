"""
This module defines the API routes for the application.
"""

from flask import Blueprint, jsonify, request

from db import db
from models.buyer import Buyer

routes = Blueprint('routes', __name__)


@routes.route('/api', methods=['GET'])
def api_endpoint():
    """
    Fetch all Buyer records from the database.

    Returns:
        JSON response containing a list of all Buyer records.
    """
    data = Buyer.query.all()
    return jsonify([item.to_dict() for item in data])


@routes.route('/add', methods=['POST'])
def add_numbers():
    """
    Add a new Buyer record to the database.

    Expects:
        JSON payload with `name` and `age` fields.

    Returns:
        JSON response containing a success message and the added Buyer record.
    """
    data = request.json
    new_entry = Buyer(name=data['name'], age=data['age'])
    db.session.add(new_entry)
    db.session.commit()
    return jsonify(
        {'message': 'Data added successfully', 'data': new_entry.to_dict()}
    )
