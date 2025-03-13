from flask import Flask
from flask_cors import CORS
from threading import Thread
import pika
import json
from db import db
from db.config import Config
from routes import routes
from socketio_instance import socketio
from services.bid_service import BidService

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

CORS(app)

socketio.init_app(app)

app.register_blueprint(routes)

# Função para consumir o lance do RabbitMQ
def consume_bid_from_rabbitmq():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='bids_queue')

    def callback(ch, method, properties, body):
        bid_data = json.loads(body)
        try:
            # Garantir que o código esteja dentro de um contexto de aplicação
            with app.app_context():  
                bidService = BidService()
                bid = bidService.create_bid(bid_data)  # Processa o lance com o BidService
                print(f"Lance processado com sucesso: {bid}")
        except Exception as e:
            print(f"Erro ao processar lance: {e}")

    channel.basic_consume(queue='bids_queue', on_message_callback=callback, auto_ack=True)
    print("Aguardando novos lances...")
    channel.start_consuming()

# Rodando o consumidor RabbitMQ em uma thread separada
def run_rabbitmq_consumer():
    consumer_thread = Thread(target=consume_bid_from_rabbitmq)
    consumer_thread.daemon = True  # Permite que o thread seja finalizado quando o programa principal terminar
    consumer_thread.start()

# Iniciar o consumidor RabbitMQ
run_rabbitmq_consumer()

# Inicialização do banco de dados
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    socketio.run(app, debug=True)
