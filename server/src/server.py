import logging

from .acceptor_socket import AcceptorSocket
from .mutable_boolean import MutableBoolean
from .server_protocol import ServerProtocol


class Server:
    def __init__(self, port, listen_backlog):
        # Initialize server socket
        self._client_sock = None
        self._acceptor_socket = AcceptorSocket('', port, listen_backlog)
        self._client_processes = []

    def run(self):
        protocol = ServerProtocol()
        socket = self._acceptor_socket.accept()
        finished_bool = MutableBoolean(False)
        while not finished_bool.get_boolean():
            action = protocol.recv_action(socket)
            action.perform_action(finished_bool)
        socket.shutdown_and_close()
        self._acceptor_socket.shutdown_and_close()
        logging.debug(f"finished")
