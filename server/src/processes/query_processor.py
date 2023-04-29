from ..acceptor_socket import AcceptorSocket
from ..communication_handlers.queue_communication_handler import QueueCommunicationHandler
from ..communication_handlers.socket_communication_handler import SocketCommunicationHandler
from ..mutable_boolean import MutableBoolean


class QueryProcessor:
    def __init__(self, port, query_queue, results_queue):
        self._query_queue = query_queue
        self._results_queue = results_queue
        self._acceptor_socket = AcceptorSocket('', port + 1, 1)

    def run(self):
        socket = self._acceptor_socket.accept()
        client_communicator_handler = SocketCommunicationHandler(socket)
        query_communication_handler = QueueCommunicationHandler(self._query_queue)
        results_communication_handler = QueueCommunicationHandler(self._results_queue)
        finished_bool = MutableBoolean(False)
        while not finished_bool.get_boolean():
            client_communicator_handler.recv_query_ask()
            results_communication_handler.send_query_ask()
            query_result = query_communication_handler.recv_query_results()
            client_communicator_handler.send_query_results(query_result)