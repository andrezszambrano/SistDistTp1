from .packet import Packet
from .server_protocol import ServerProtocol


class CommunicationHandler:
    def __init__(self, socket):
        self._socket = socket

    def send_ack(self):
        packet = Packet()
        protocol = ServerProtocol()
        protocol.add_ack_to_packet(packet)
        self._socket.send(packet)

    def recv_action(self):
        protocol = ServerProtocol()
        return protocol.recv_action(self._socket)

    def recv_data_distributer_action(self, queue):
        protocol = ServerProtocol()
        packet = queue.pop()
        return protocol.recv_data_distributer_action(packet)

