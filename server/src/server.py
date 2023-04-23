import logging
from multiprocessing import Process

from .acceptor_socket import AcceptorSocket
from .data_distributer import DataDistributer
from .mutable_boolean import MutableBoolean
from .queues.prod_cons_queue import ProdConsQueue
from .server_protocol import ServerProtocol


class Server:
    def __init__(self, port, listen_backlog):
        # Initialize server socket
        self._client_sock = None
        self._acceptor_socket = AcceptorSocket('', port, listen_backlog)
        self._client_processes = []
        self._prod_cons_queue = ProdConsQueue()

    def run(self):
        protocol = ServerProtocol()
        socket = self._acceptor_socket.accept()
        finished_bool = MutableBoolean(False)
        data_distributer = DataDistributer(self._prod_cons_queue)
        data_distributer_process = Process(target=data_distributer.run, args=(), daemon=True)
        data_distributer_process.start()
        while not finished_bool.get_boolean():
            action = protocol.recv_action(socket)
            action.perform_action(finished_bool, self._prod_cons_queue)
        socket.shutdown_and_close()
        self._acceptor_socket.shutdown_and_close()
        logging.debug(f"finished")
