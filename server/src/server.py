import logging

from .acceptor_socket import AcceptorSocket
from .mutable_boolean import MutableBoolean
from .communication_handler import CommunicationHandler


class Server:
    def __init__(self, port, listen_backlog):
        # Initialize server socket
        self._client_sock = None
        self._acceptor_socket = AcceptorSocket('', port, listen_backlog)
        self._client_processes = []

    def run(self):
        socket = self._acceptor_socket.accept()
        communication_handler = CommunicationHandler(socket)
        finished_bool = MutableBoolean(False)
        while not finished_bool.get_boolean():
            action = communication_handler.recv_action()
            action.perform_action(finished_bool, communication_handler)
        socket.shutdown_and_close()
        self._acceptor_socket.shutdown_and_close()
        logging.debug(f"finished")
