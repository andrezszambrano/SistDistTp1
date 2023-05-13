import logging
import time

import pika


class RabbitInitializer:
    DELAY_BETWEEN_ATTEMPTS = 4
    MAX_ATTEMPTS = 5

    def __init__(self):
        attempts = 0
        while attempts < self.MAX_ATTEMPTS:
            try:
                self._connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
                break
            except pika.exceptions.AMQPConnectionError as _e:
                logging.debug("Error connecting to RabbitMQ broker")
                time.sleep(self.DELAY_BETWEEN_ATTEMPTS)
                attempts += 1

    def get_channel(self):
        return self._connection.channel()
