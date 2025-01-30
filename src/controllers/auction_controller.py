# pylint: disable=broad-except,line-too-long
"""
Module providing auction-related API endpoints.
Handles creating auctions and retrieving them based on various filters.
"""

from datetime import datetime
from flask import Blueprint, jsonify, request

from models.status import Status
from services.auction_service import AuctionService

auctionService = AuctionService()


auction_bp = Blueprint('auction', __name__, url_prefix='/auction')


def validate_auction_data(data, required_fields):
    """Validate auction data against required fields."""
    if not data or not all(field in data for field in required_fields):
        raise ValueError('Invalid input, missing required fields')


@auction_bp.route('/create', methods=['POST'])
def create_auction_endpoint():
    """
    Endpoint to create a new auction.

    Request Body:
        {
            "title": "Auction for Item XYZ",
            "start_date": "2024-12-20T10:00:00",
            "end_date": "2024-12-21T10:00:00",
            "initial_value": 100.00,
            "min_increment": 5.00,
            ...
        }

    Returns:
        JSON response with the created auction or error message.
    """
    data = request.get_json()
    required_fields = [
        'title',
        'end_date',
        'initial_value',
        'min_increment',
        'item_id',
        'type_id',
        'seller_id'
    ]

    try:
        validate_auction_data(data, required_fields)

        data['status'] = Status['PENDING']

        auction = auctionService.create_auction(data)
        return jsonify(auction.to_dict()), 201
    except ValueError as val_err:
        return jsonify({'error': str(val_err)}), 400
    except Exception as gen_err:
        return jsonify({'error': str(gen_err)}), 500


@auction_bp.route('/list', methods=['GET'])
def list_auctions():
    """
    Endpoint to list auctions with pagination and optional filters.

    Query Parameters:
        page (int): The page number for pagination (default is 1).
        per_page (int): The number of items per page (default is 10).
        title (str, optional): Filter by auction title.
        category_id (int, optional): Filter by category.
        type_id (int, optional): Filter by auction type.
        status (str, optional): Filter by auction status.
        min_bid (float, optional): Filter auctions with a minimum bid.
        max_bid (float, optional): Filter auctions with a maximum bid.
        end_date (str, optional): Filter auctions ending on a specific date.

    Returns:
        JSON response with paginated list of auctions.
    """
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    filters = {
        'title': request.args.get('title', type=str),
        'category_id': request.args.get('category_id', type=int),
        'type_id': request.args.get('type_id', type=int),
        'status': request.args.get('status', type=str),
        'min_bid': request.args.get('min_bid', type=float),
        'max_bid': request.args.get('max_bid', type=float),
        'end_date': request.args.get('end_date', type=str),
    }

    filters = {k: v for k, v in filters.items() if v is not None}

    if 'end_date' in filters:
        filters['end_date'] = datetime.fromisoformat(filters['end_date'])

    try:
        auctions = auctionService.get_all_auctions(page, per_page, filters)
        return jsonify([auction.to_dict() for auction in auctions.items]), 200
    except Exception as gen_err:
        return jsonify({'error': str(gen_err)}), 500


@auction_bp.route('/list/<int:auction_id>', methods=['GET'])
def get_auction(auction_id):
    """
    Endpoint to fetch details of a specific auction by ID.

    Returns:
        JSON response with the auction details or error message if not found.
    """
    try:
        auction = auctionService.get_auction_by_id(auction_id)
        if auction:
            return jsonify(auction.to_dict()), 200
        return jsonify({'error': 'Auction not found'}), 404
    except Exception as gen_err:
        return jsonify({'error': str(gen_err)}), 500


@auction_bp.route('/list_by_status/<int:status_id>', methods=['GET'])
def fetch_auctions_by_status(status_id):
    """
    Endpoint to fetch auctions by status_id with pagination.

    Query Parameters:
        page (int): The page number for pagination (default is 1).
        per_page (int): The number of items per page (default is 10).

    Returns:
        JSON response with paginated list of auctions for the given status_id.
    """
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    try:
        auctions = auctionService.get_auctions_by_status(
            status_id, page, per_page
        )
        return jsonify([auction.to_dict() for auction in auctions.items]), 200
    except Exception as gen_err:
        return jsonify({'error': str(gen_err)}), 500
    
@auction_bp.route('/user/<int:user_id>', methods=['GET'])
def get_auctions_by_user_bids(user_id):
    """
    Endpoint to fetch auctions by user with pagination.

    Query Parameters:
        page (int): The page number for pagination (default is 1).
        per_page (int): The number of items per page (default is 10).

    Returns:
        JSON response with paginated auctions by user.
    """
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    try:
        auctions = auctionService.get_auctions_by_user_bids(user_id, page, per_page)
        return jsonify([auction.to_dict() for auction in auctions.items]), 200
    except Exception as gen_err:
        return jsonify({'error': str(gen_err)}), 500
