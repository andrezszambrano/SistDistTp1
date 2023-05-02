

class RabbPublSubsQueueRecv:
    def __init__(self, channel, exchange_name):
        self._channel = channel
        self._exchange_name = exchange_name
        channel.exchange_declare(exchange=exchange_name, exchange_type='fanout')
        result = channel.queue_declare(queue='')
        channel.queue_bind(exchange=exchange_name, queue=result.method.queue)

