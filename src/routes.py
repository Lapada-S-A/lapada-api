from flask import Blueprint, jsonify, request
from models import Buyer
from db import db

routes = Blueprint('routes', __name__)

@routes.route('/api', methods=['GET'])
def api_endpoint():
    data = Buyer.query.all()
    return jsonify([item.to_dict() for item in data])

@routes.route('/add', methods=['POST'])
def add_numbers():
    data = request.json
    new_entry = Buyer(name=data['name'], age=data['age'])
    db.session.add(new_entry)
    db.session.commit()
    return jsonify({"message": "Data added successfully", "data": new_entry.to_dict()})
 