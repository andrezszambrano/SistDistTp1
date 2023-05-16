import logging
import signal

from .acceptor_socket import AcceptorSocket
from .queue_communication_handler import QueueCommunicationHandler
from .socket_communication_handler import SocketCommunicationHandler
from .mutable_boolean import MutableBoolean
from .rabb_prod_cons_queue import RabbProdConsQueue


class ClientMainApiProcessor:
    def __init__(self, port, listen_backlog, channel):
        # Initialize server socket
        self._client_sock = None
        self._port = port
        self._acceptor_socket = AcceptorSocket('', port, listen_backlog)
        self._client_processes = []
        self._channel = channel
        self._finished_bool = MutableBoolean(False)
        queue_for_all_data = RabbProdConsQueue(channel, "AllData")
        self._all_data_sender_communication_handler = QueueCommunicationHandler(queue_for_all_data)
        socket = self._acceptor_socket.accept()
        self._client_communicator_handler = SocketCommunicationHandler(socket)
        signal.signal(signal.SIGTERM, self.__exit_gracefully)

    def __exit_gracefully(self, _signum, _frame):
        logging.info("Exiting gracefully")
        self.__close_resources()

    def run(self):
        while not self._finished_bool.get_boolean():
            action = self._client_communicator_handler.recv_action()
            action.perform_action(self._finished_bool, self._client_communicator_handler,
                                  self._all_data_sender_communication_handler)
        self.__close_resources()
        logging.debug(f"finished")

    def __close_resources(self):
        self._client_communicator_handler.close()
        self._all_data_sender_communication_handler.close()
        self._acceptor_socket.shutdown_and_close()
        self._channel.close()