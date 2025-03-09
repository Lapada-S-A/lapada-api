from datetime import datetime
import json
from flask import Blueprint, request, jsonify
from flask_socketio import SocketIO, emit

from models.chat import create_chat, get_chat, create_message, get_messages_from_chat, redis_client
from socketio_instance import socketio

chat_bp = Blueprint("chat", __name__, url_prefix='/chat')


@chat_bp.route("/create", methods=["POST"])
def create_chat_route():
    data = request.json
    users = data.get("users")
    if not users or len(users) < 2:
        return jsonify({"error": "Chat deve ter pelo menos dois usuários"}), 400

    chat_id = len(redis_client.keys("chat:*")) + 1 
    create_chat(chat_id, users)

    return jsonify({"chat_id": chat_id, "users": users}), 201

@chat_bp.route("/message", methods=["POST"])
def send_message_route():
    data = request.json
    chat_id = data.get("chat_id")
    sender_id = data.get("sender_id")
    content = data.get("content")
    
    if not chat_id or not sender_id or not content:
        return jsonify({"error": "Faltando informações"}), 400

    chat = get_chat(chat_id)
    if not chat:
        return jsonify({"error": "Chat não encontrado"}), 404

    message_id = len(redis_client.keys("message:*")) + 1
    create_message(message_id, chat_id, sender_id, content)
    
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    chat["last_message"] = {"message_id": message_id, "sender_id": sender_id, "content": content, "date": current_time}
    redis_client.set(f"chat:{chat_id}", json.dumps(chat))

    socketio.emit('new_message', {
        'chat_id': chat_id,
        'message_id': message_id,
        'sender_id': sender_id,
        'content': content,
        'date': current_time
    })

    return jsonify({
        "message_id": message_id,
        "sender_id": sender_id,
        "content": content,
        "date": current_time
    }), 201

@chat_bp.route("/<int:chat_id>/messages", methods=["GET"])
def get_messages_route(chat_id):
    chat = get_chat(chat_id)
    if not chat:
        return jsonify({"error": "Chat não encontrado"}), 404

    messages = get_messages_from_chat(chat_id)
    return jsonify(messages)

@socketio.on('connect')
def handle_connect():
    emit('status', {'msg': 'Cliente conectado'})

@socketio.on('disconnect')
def handle_disconnect():
    emit('status', {'msg': 'Cliente desconectado'})
