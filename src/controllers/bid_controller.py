# pylint: disable=broad-except
"""
Bid module endpoints for creating and listing bids.
"""
from flask import Blueprint, jsonify, request

from models.bid import Bid
from services.bid_service import BidService

bidService = BidService()

bid_bp = Blueprint('bid', __name__, url_prefix='/bid')


@bid_bp.route('/create', methods=['POST'])
def create_bid_endpoint():
    """
    Endpoint to create a new bid.

    Request Body:
        {
            "amount": 150.00,
            "auction_id": 1,
            "buyer_id": 2,
            "bid_status_id": 1
        }

    Returns:
        JSON response with the created bid or error message.
    """
    data = request.get_json()

    required_fields = ['amount', 'auction_id', 'buyer_id', 'bid_status_id']
    if not data or not all(field in data for field in required_fields):
        return (
            jsonify({'error': 'Invalid input, missing required fields'}),
            400,
        )

    try:
        bid = bidService.create_bid(data)
        return jsonify(bid.to_dict()), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@bid_bp.route('/list/<int:auction_id>', methods=['GET'])
def list_bids_for_auction(auction_id):
    """
    Endpoint to list all bids or the top bids for a specific auction.

    Query Parameters:
        limit (int): The number of top bids to return (optional).

    Returns:
        JSON response with the list of bids or an error message.
    """
    limit = request.args.get('limit', None, type=int)

    try:
        # Base query to filter bids by auction_id
        query = Bid.query.filter_by(auction_id=auction_id).order_by(
            Bid.amount.desc()
        )

        # Apply limit if provided
        if limit is not None:
            bids = query.limit(limit).all()
        else:
            bids = query.all()

        return jsonify([bid.to_dict() for bid in bids]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400
