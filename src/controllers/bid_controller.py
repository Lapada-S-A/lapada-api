# pylint: disable=broad-except
"""
Bid module endpoints for creating and listing bids.
"""
import json
from flask import Blueprint, jsonify, request
import pika

from models.bid import Bid
from services.bid_service import BidService

bidService = BidService()

bid_bp = Blueprint('bid', __name__, url_prefix='/bid')


def send_bid_to_rabbitmq(data):
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        channel.queue_declare(queue='bids_queue')

        message = json.dumps(data)
        channel.basic_publish(exchange='', routing_key='bids_queue', body=message)

        connection.close()
    except Exception as e:
        raise Exception(f"Erro ao enviar para RabbitMQ: {str(e)}")
    
def consume_bid_from_rabbitmq():
    """Consumir a mensagem do RabbitMQ e processar o lance."""
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='bids_queue')

    def callback(ch, method, properties, body):
        bid_data = json.loads(body)
        try:
            bid = bidService.create_bid(bid_data)
            print(f"Lance processado com sucesso: {bid}")
        except Exception as e:
            print(f"Erro ao processar lance: {e}")

    channel.basic_consume(queue='bids_queue', on_message_callback=callback, auto_ack=True)

    channel.start_consuming()

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

    required_fields = ['amount', 'auction_id', 'buyer_id']
    if not data or not all(field in data for field in required_fields):
        return jsonify({'message': 'Input inválido, campos obrigatórios faltando'}), 400

    try:
        send_bid_to_rabbitmq(data)

        return jsonify({'message': 'Bid enviado para o RabbitMQ'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 400


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
        query = Bid.query.filter_by(auction_id=auction_id).order_by(
            Bid.amount.desc()
        )

        if limit is not None:
            bids = query.limit(limit).all()
        else:
            bids = query.all()

        return jsonify([bid.to_dict() for bid in bids]), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 400

@bid_bp.route("list/auction/<int:auction_id>/buyer/<int:buyer_id>", methods=["GET"])
def get_bids_by_buyer_in_auction(auction_id, buyer_id):
    """
    Endpoint para listar todos os lances feitos por um comprador em um leilão específico.

    Args:
        auction_id (int): ID do leilão.
        buyer_id (int): ID do comprador.

    Returns:
        JSON: Lista de lances do comprador no leilão.
    """
    page = request.args.get("page", default=1, type=int)
    per_page = request.args.get("per_page", default=10, type=int)

    bids = BidService.get_bids_by_buyer_in_auction(auction_id, buyer_id, page, per_page)

    bids_dto = [
        {
            "id": bid.id,
            "amount": bid.amount,
            "bid_date": bid.bid_date.strftime('%d-%m-%Y-%H-%M-%S'),
            "bid_status": bid.bid_status.value
        }
        for bid in bids
    ]

    return jsonify({
        "bids": [bid for bid in bids_dto],
        "total": bids.total,
        "page": bids.page,
        "per_page": bids.per_page,
        "pages": bids.pages
    })
