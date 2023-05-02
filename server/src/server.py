import logging
from multiprocessing import Process

from .acceptor_socket import AcceptorSocket
from .communication_handlers.queue_communication_handler import QueueCommunicationHandler
from .communication_handlers.socket_communication_handler import SocketCommunicationHandler
from .processes.data_distributer import DataDistributer
from .processes.query_processor import QueryProcessor
from .processes.result_processor import ResultMonitorProcessor
from .mutable_boolean import MutableBoolean
from .queues.prod_cons_queue import ProdConsQueue


class Server:
    def __init__(self, port, listen_backlog, channel):
        # Initialize server socket
        self._client_sock = None
        self._port = port
        self._acceptor_socket = AcceptorSocket('', port, listen_backlog)
        self._client_processes = []
        self._channel = channel
        self._prod_cons_queue = ProdConsQueue()
        self._results_monitor_queue = ProdConsQueue()
        self._query_queue = ProdConsQueue()

    def run(self):
        socket = self._acceptor_socket.accept()
        client_communicator_handler = SocketCommunicationHandler(socket)
        distributor_communicator_handler = QueueCommunicationHandler(queue=self._prod_cons_queue)
        finished_bool = MutableBoolean(False)
        data_distributer_process = self.__create_and_run_data_distributer_process()
        query_processor = self.__create_and_run_query_processor()
        result_monitor_processor = self.__create_and_run_results_processor()
        while not finished_bool.get_boolean():
            action = client_communicator_handler.recv_action()
            action.perform_action(finished_bool, client_communicator_handler, distributor_communicator_handler)
        data_distributer_process.join()
        result_monitor_processor.join()
        query_processor.join()
        socket.shutdown_and_close()
        self._acceptor_socket.shutdown_and_close()
        logging.debug(f"finished")

    def __create_and_run_data_distributer_process(self):
        data_distributer = DataDistributer(self._prod_cons_queue, self._results_monitor_queue, self._channel)
        data_distributer_process = Process(target=data_distributer.run, args=(), daemon=False)
        data_distributer_process.start()
        return data_distributer_process

    def __create_and_run_results_processor(self):
        result_monitor_processor = ResultMonitorProcessor(self._results_monitor_queue, self._query_queue)
        result_monitor_processor_process = Process(target=result_monitor_processor.run, args=(), daemon=False)
        result_monitor_processor_process.start()
        return result_monitor_processor_process

    def __create_and_run_query_processor(self):
        query_processor = QueryProcessor(self._port, self._query_queue, self._results_monitor_queue)
        query_processor_process = Process(target=query_processor.run, args=(), daemon=False)
        query_processor_process.start()
        return query_processor_process
