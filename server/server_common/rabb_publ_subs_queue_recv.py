

class RabbPublSubsQueueRecv:
    def __init__(self, channel, exchange_name, callback):
        self._channel = channel
        self._exchange_name = exchange_name
        channel.exchange_declare(exchange=exchange_name, exchange_type='fanout')
        result = channel.queue_declare(queue='', exclusive=True)
        queue_name = result.method.queue
        channel.queue_bind(exchange=exchange_name, queue=queue_name)
        channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

    def start_recv_loop(self):
        self._channel.start_consuming()
