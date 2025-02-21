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
        'description',
        'end_date',
        'initial_value',
        'min_increment',
        'seller_id',
        'type_id'
    ]

    try:
        validate_auction_data(data, required_fields)

        data['status'] = Status['PENDING']

        auction = auctionService.create_auction(data)
        auctionService.add_categories_to_auction(auction.id, data.get('categories', []))
        return jsonify(auction.to_dict()), 201
    except ValueError as val_err:
        return jsonify({'error': str(val_err)}), 400
    except Exception as gen_err:
        return jsonify({'error': str(gen_err)}), 500


@auction_bp.route('/list', methods=['GET'])
def list_auctions():
    """
    Endpoint to list auctions with optional pagination and filters.
    """
    page = request.args.get('page', type=int)
    per_page = request.args.get('per_page', type=int)

    filters = {
        'title': request.args.get('title', type=str),
        'category_id': request.args.get('category_id', type=int),
        'type_id': request.args.get('type_id', type=int),
        'status': request.args.get('status', type=str),
        'min_bid': request.args.get('min_bid', type=float),
        'max_bid': request.args.get('max_bid', type=float),
        'end_date': request.args.get('end_date', type=str),
        'description': request.args.get('description', type=str),
    }

    filters = {k: v for k, v in filters.items() if v is not None}

    try:
        auctions = auctionService.get_all_auctions(page, per_page, filters)

        # Se for uma lista normal, formata direto
        if isinstance(auctions, list):
            return jsonify([auction.to_dict(highest_bid=auctionService.get_highest_bid(auction_id=auction.id)) for auction in auctions]), 200
        
        # Caso contrário, assume que é um objeto paginado
        response = {
            'items': [auction.to_dict(highest_bid=auctionService.get_highest_bid(auction_id=auction.id)) for auction in auctions.items],
            'pagination': {
                'page': auctions.page,
                'per_page': auctions.per_page,
                'total': auctions.total,
            }
        }
        return jsonify(response), 200

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
            return jsonify(auction.to_dict(highest_bid=auctionService.get_highest_bid(auction_id=auction.id))), 200
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

        response = {
            'items': [auction.to_dict(highest_bid=auctionService.get_highest_bid(auction_id=auction.id)) for auction in auctions.items],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': auctions.total,  # Assuming `total` is provided by the service
            }
        }

        return jsonify(response), 200

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

        response = {
            'items': [auction.to_dict(highest_bid=auctionService.get_highest_bid(auction_id=auction.id)) for auction in auctions.items],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': auctions.total,
            }
        }

        return jsonify(response), 200

    except Exception as gen_err:
        return jsonify({'error': str(gen_err)}), 500

@auction_bp.route('/approve/<int:auction_id>', methods=['POST'])
def approve_auction(auction_id):
    """
    Endpoint to change change auction status to active.

    Returns:
        JSON response with the updated auction or error message.
    """
    try:
        auction = auctionService.get_auction_by_id(auction_id)
        auction = auctionService.update_auction_status(auction, Status.ACTIVE, Status.PENDING)
        return jsonify(auction.to_dict()), 201
    except ValueError as val_err:
        return jsonify({'error': str(val_err)}), 400
    except Exception as gen_err:
        return jsonify({'error': str(gen_err)}), 500

@auction_bp.route('/reject/<int:auction_id>', methods=['POST'])
def reject_auction(auction_id):
    """
    Endpoint to change change auction status to rejected.

    Returns:
        JSON response with the updated auction or error message.
    """
    try:
        auction = auctionService.get_auction_by_id(auction_id)
        auction = auctionService.update_auction_status(auction, Status.REJECTED, Status.PENDING)
        return jsonify(auction.to_dict()), 201
    except ValueError as val_err:
        return jsonify({'error': str(val_err)}), 400
    except Exception as gen_err:
        return jsonify({'error': str(gen_err)}), 500
    
@auction_bp.route('/finish/<int:auction_id>', methods=['PATCH'])
def finish_auction(auction_id):
    """
    Endpoint para finalizar um leilão.
    """
    try:
        auction = auctionService.finish_auction(auction_id)
        return jsonify(auction.to_dict()), 201
    except ValueError as val_err:
        return jsonify({'error': str(val_err)}), 400
    except Exception as gen_err:
        return jsonify({'error': str(gen_err)}), 500


@auction_bp.route('/cancel/<int:auction_id>', methods=['PATCH'])
def cancel_auction(auction_id):
    """
    Endpoint para cancelar um leilão.
    """
    try:
        auction = auctionService.cancel_auction(auction_id)
        return jsonify(auction.to_dict()), 201
    except ValueError as val_err:
        return jsonify({'error': str(val_err)}), 400
    except Exception as gen_err:
        return jsonify({'error': str(gen_err)}), 500


@auction_bp.route('/seller/<int:seller_id>', methods=['GET'])
def get_auctions_by_seller(seller_id):
    """
    Endpoint to retrieve all auctions for a specific seller.

    Returns:
        JSON response with auction details or error message.
    """
    try:
        auctions = auctionService.get_auctions_by_seller(seller_id)
        return jsonify(auctions), 200
    except Exception as gen_err:
        return jsonify({'error': str(gen_err)}), 500

@auction_bp.route('/update/<int:auction_id>', methods=['PUT'])
def update_auction(auction_id):
    """
    Endpoint to update an auction.
    """
    data = request.get_json()
    print(data)

    try:
        auction = auctionService.update_auction(auction_id, data)
        return jsonify(auction.to_dict()), 200
    except ValueError as val_err:
        return jsonify({'error': str(val_err)}), 400
    except Exception as gen_err:
        return jsonify({'error': str(gen_err)}), 500

@auction_bp.route("/buyer/<int:buyer_id>", methods=["GET"])
def get_auctions_by_buyer(buyer_id):
    """
    Endpoint para listar os leilões em que um comprador participou com lances.

    Args:
        buyer_id (int): ID do comprador.

    Returns:
        JSON: Lista paginada de leilões.
    """
    page = request.args.get("page", default=1, type=int)
    per_page = request.args.get("per_page", default=10, type=int)

    auctions = AuctionService.get_auctions_by_user_bids(buyer_id, page, per_page)

    return jsonify({
        "auctions": [auction.to_dict(highest_bid=auctionService.get_highest_bid(auction_id=auction.id)) for auction in auctions.items],
        "total": auctions.total,
        "page": auctions.page,
        "per_page": auctions.per_page,
        "pages": auctions.pages
    })
