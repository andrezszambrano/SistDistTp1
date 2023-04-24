from .packet import Packet
from .server_protocol import ServerProtocol


class CommunicationHandler:
    def __init__(self, socket=None, queue=None):
        self._socket = socket
        self._queue = queue

    def send_ack(self):
        packet = Packet()
        protocol = ServerProtocol()
        protocol.add_ack_to_packet(packet)
        self._socket.send(packet)

    def send_finished(self):
        packet = Packet()
        protocol = ServerProtocol()
        protocol.add_finished_to_packet(packet)
        self._queue.send(packet)

    def recv_action(self):
        protocol = ServerProtocol()
        return protocol.recv_action(self._socket)

    def send_data_to_distributer(self, data_type, city_name, data):
        packet = Packet()
        protocol = ServerProtocol()
        protocol.add_data_to_packet(packet, data_type, city_name, data)
        self._queue.send(packet)

    def recv_data_distributer_action(self, queue):
        protocol = ServerProtocol()
        packet = queue.get_packet()
        return protocol.recv_data_distributer_action(packet)
