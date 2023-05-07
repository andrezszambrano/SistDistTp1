import pika

class RabbitInitializer:
    def __init__(self):
        self._connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))

    def get_channel(self):
        return self._connection.channel()

