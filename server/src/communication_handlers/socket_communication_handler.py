import logging

from ..packet import Packet
from .communication_handler import CommunicationHandler
from ..server_protocol import ServerProtocol


class SocketCommunicationHandler(CommunicationHandler):

    def __init__(self, socket):
        super(SocketCommunicationHandler).__init__()
        self._socket = socket

    def send_ack(self):
        packet = Packet()
        protocol = ServerProtocol()
        protocol.add_ack_to_packet(packet)
        self._socket.send(packet)

    def recv_action(self):
        protocol = ServerProtocol()
        return protocol.recv_action(self._socket)