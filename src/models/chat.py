from datetime import datetime
import redis
import json
from datetime import datetime

class Chat:
    def __init__(self, chat_id, users, last_message):
        self.chat_id = chat_id
        self.users = users
        self.last_message = last_message

class Message:
    def __init__(self, message_id, sender_id, content, date=None):
        self.message_id = message_id
        self.sender_id = sender_id
        self.content = content
        self.date = date or datetime.now()


redis_client = redis.StrictRedis(host="localhost", port=6379, db=0, decode_responses=True)

def create_chat(chat_id, users):
    chat = {"chat_id": chat_id, "users": users, "last_message": None}
    redis_client.set(f"chat:{chat_id}", json.dumps(chat))

def get_chat(chat_id):
    chat_data = redis_client.get(f"chat:{chat_id}")
    if chat_data:
        return json.loads(chat_data)
    return None

def create_message(message_id, chat_id, sender_id, content):
    message = {
        "message_id": message_id,
        "chat_id": chat_id,
        "sender_id": sender_id,
        "content": content,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    redis_client.set(f"message:{message_id}", json.dumps(message))
    redis_client.rpush(f"chat:{chat_id}:messages", message_id)  

def get_messages_from_chat(chat_id):
    message_ids = redis_client.lrange(f"chat:{chat_id}:messages", 0, -1)
    messages = []
    for message_id in message_ids:
        message_data = redis_client.get(f"message:{message_id}")
        if message_data:
            messages.append(json.loads(message_data))
    return messages
