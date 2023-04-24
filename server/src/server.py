import logging
from multiprocessing import Process

from .acceptor_socket import AcceptorSocket
from .communication_handlers.queue_communication_handler import QueueCommunicationHandler
from .communication_handlers.socket_communication_handler import SocketCommunicationHandler
from .data_distributer import DataDistributer
from .mutable_boolean import MutableBoolean
from .queues.prod_cons_queue import ProdConsQueue


class Server:
    def __init__(self, port, listen_backlog):
        # Initialize server socket
        self._client_sock = None
        self._acceptor_socket = AcceptorSocket('', port, listen_backlog)
        self._client_processes = []
        self._prod_cons_queue = ProdConsQueue()

    def run(self):
        socket = self._acceptor_socket.accept()
        client_communicator_handler = SocketCommunicationHandler(socket)
        distributor_communicator_handler = QueueCommunicationHandler(queue=self._prod_cons_queue)
        finished_bool = MutableBoolean(False)
        data_distributer_process = self.__run_data_distributer_process()
        while not finished_bool.get_boolean():
            action = client_communicator_handler.recv_action()
            action.perform_action(finished_bool, client_communicator_handler, distributor_communicator_handler)
        data_distributer_process.join()
        socket.shutdown_and_close()
        self._acceptor_socket.shutdown_and_close()
        logging.debug(f"finished")

    def __run_data_distributer_process(self):
        data_distributer = DataDistributer(self._prod_cons_queue)
        data_distributer_process = Process(target=data_distributer.run, args=(), daemon=True)
        data_distributer_process.start()
        return data_distributer_process
