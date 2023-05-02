import logging

from .acceptor_socket import AcceptorSocket
from .communication_handlers.queue_communication_handler import QueueCommunicationHandler
from .communication_handlers.socket_communication_handler import SocketCommunicationHandler
from .mutable_boolean import MutableBoolean
from .queues.prod_cons_queue import ProdConsQueue
from .queues.rabb_prod_cons_queue import RabbProdConsQueue


class Server:
    def __init__(self, port, listen_backlog, channel):
        # Initialize server socket
        self._client_sock = None
        self._port = port
        self._acceptor_socket = AcceptorSocket('', port, listen_backlog)
        self._client_processes = []
        self._channel = channel
        self._queue_for_all_data = RabbProdConsQueue(channel, "AllData")

    def run(self):
        socket = self._acceptor_socket.accept()
        client_communicator_handler = SocketCommunicationHandler(socket)
        distributor_communicator_handler = QueueCommunicationHandler(queue=self._queue_for_all_data)
        finished_bool = MutableBoolean(False)
        #data_distributer_process = self.__create_and_run_data_distributer_process()
        #query_processor = self.__create_and_run_query_processor()
        #result_monitor_processor = self.__create_and_run_results_processor()
        while not finished_bool.get_boolean():
            action = client_communicator_handler.recv_action()
            action.perform_action(finished_bool, client_communicator_handler, distributor_communicator_handler)
        #data_distributer_process.join()
        #result_monitor_processor.join()
        #query_processor.join()
        socket.shutdown_and_close()
        self._acceptor_socket.shutdown_and_close()
        logging.debug(f"finished")
