import pika

class RabbitInitializer:
    def __init__(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
        self._channel = connection.channel()

    def get_channel(self):
        return self._channel
