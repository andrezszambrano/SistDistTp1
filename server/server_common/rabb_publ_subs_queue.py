from .packet_sender import PacketSender


class RabbPublSubsQueue(PacketSender):
    def __init__(self, rabbit_channel_wrapper, exchange_name, callback=None):
        self._channel = rabbit_channel_wrapper.channel
        self._exchange_name = exchange_name
        self._channel.exchange_declare(exchange=exchange_name, exchange_type='fanout')
        self._closed = False
        if callback is not None:
            result = self._channel.queue_declare(queue='', exclusive=True)
            queue_name = result.method.queue
            self._channel.queue_bind(exchange=exchange_name, queue=queue_name)
            self._channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

    def start_recv_loop(self):
        if not self._closed:
            self._channel.start_consuming()

    def send(self, packet):
        if not self._closed:
            self._channel.basic_publish(exchange=self._exchange_name, routing_key='', body=packet.get_bytes())

    def close(self):
        self._closed = True
