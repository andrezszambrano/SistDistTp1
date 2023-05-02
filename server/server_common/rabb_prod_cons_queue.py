
from .packet_sender import PacketSender


class RabbProdConsQueue(PacketSender):
    def __init__(self, channel, queue_name, callback=None):
        super(RabbProdConsQueue, self).__init__()
        self._channel = channel
        self._channel.queue_declare(queue=queue_name)
        self._queue_name = queue_name
        if callback is not None:
            channel.basic_consume(queue=self._queue_name, on_message_callback=callback, auto_ack=True)

    def start_recv_loop(self):
        self._channel.start_consuming()

    def send(self, packet):
        self._channel.basic_publish(exchange="", routing_key=self._queue_name, body=packet.get_bytes())
