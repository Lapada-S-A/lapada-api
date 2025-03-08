from datetime import datetime
import json
from flask import Blueprint, request, jsonify
from models.chat import create_chat, get_chat, create_message, get_messages_from_chat, redis_client

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
