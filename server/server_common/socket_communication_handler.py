import logging

from .packet import Packet
from .server_protocol import ServerProtocol


class SocketCommunicationHandler:

    def __init__(self, socket):
        self._socket = socket

    def send_ack(self):
        packet = Packet()
        protocol = ServerProtocol()
        protocol.add_ack_to_packet(packet)
        self._socket.send(packet)

    def send_query_results(self, query_results):
        packet = Packet()
        protocol = ServerProtocol()
        protocol.add_query_results_to_packet(packet, query_results)
        self._socket.send(packet)

    def recv_action(self):
        protocol = ServerProtocol()
        return protocol.recv_action(self._socket)

    def recv_query_ask(self):
        protocol = ServerProtocol()
        return protocol.recv_query_ask(self._socket)
