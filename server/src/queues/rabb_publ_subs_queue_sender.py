from ..packet_sender import PacketSender


class RabbPublSubsQueueSender(PacketSender):
    def __init__(self, channel, exchange_name):
        self._channel = channel
        self._exchange_name = exchange_name
        channel.exchange_declare(exchange=exchange_name, exchange_type='fanout')

    def send(self, packet):
        self._channel.basic_publish(exchange=self._exchange_name, routing_key='', body=packet.get_bytes())
