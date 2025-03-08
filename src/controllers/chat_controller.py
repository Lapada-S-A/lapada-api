from flask import Blueprint, request, jsonify
from flask_socketio import SocketIO
from models.chat import Chat, Message, chats, messages
import redis

chat_bp = Blueprint("chat", __name__, url_prefix='/chat')

# Criar chat
@chat_bp.route("/create", methods=["POST"])
def create_chat():
    data = request.json
    users = data.get("users")
    if not users or len(users) < 2:
        return jsonify({"error": "Chat deve ter pelo menos dois usuários"}), 400

    chat_id = len(chats) + 1  # ID simples baseado no número de chats
    chat = Chat(chat_id, users, None)
    chats[chat_id] = chat

    return jsonify({"chat_id": chat.chat_id, "users": chat.users}), 201

# Enviar mensagem
@chat_bp.route("/message", methods=["POST"])
def send_message():
    data = request.json
    chat_id = data.get("chat_id")
    sender_id = data.get("sender_id")
    content = data.get("content")
    
    if not chat_id or not sender_id or not content:
        return jsonify({"error": "Faltando informações"}), 400

    # Verificar se o chat existe
    chat = chats.get(chat_id)
    if not chat:
        return jsonify({"error": "Chat não encontrado"}), 404

    # Criar mensagem
    message_id = len(messages) + 1
    message = Message(message_id, sender_id, content)
    messages[message_id] = message
    
    # Atualizar último chat
    chat.last_message = message

    return jsonify({
        "message_id": message.message_id,
        "sender_id": message.sender_id,
        "content": message.content,
        "date": message.date.strftime("%Y-%m-%d %H:%M:%S")
    }), 201

# Obter mensagens do chat
@chat_bp.route("/<int:chat_id>/messages", methods=["GET"])
def get_messages(chat_id):
    chat = chats.get(chat_id)
    if not chat:
        return jsonify({"error": "Chat não encontrado"}), 404

    chat_messages = [msg for msg in messages.values() if msg.sender_id in chat.users]
    return jsonify([{
        "message_id": msg.message_id,
        "sender_id": msg.sender_id,
        "content": msg.content,
        "date": msg.date.strftime("%Y-%m-%d %H:%M:%S")
    } for msg in chat_messages])
