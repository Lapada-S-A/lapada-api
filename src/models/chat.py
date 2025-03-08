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

# Dados simulados
chats = {}
messages = {}
