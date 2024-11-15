from flask import Blueprint, jsonify, request

routes = Blueprint('routes', __name__)

@routes.route('/api', methods=['GET'])
def api_endpoint():
    return jsonify({"message": "Hello, World!"})

@routes.route('/add', methods=['POST'])
def add_numbers():
    data = request.json
    return jsonify({"result": data})
