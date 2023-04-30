import time

from .client_communication_handler import ClientCommunicationHandler
from .mutable_boolean import MutableBoolean
from .socket_wrapper import Socket


class QueryAsker:
    MAX_ATTEMPTS = 5
    DELAY_BETWEEN_ATTEMPTS = 3
    WAIT = 20

    def __init__(self, server_address):
        self._host, _port = server_address.split(':')
        self._port = int(_port) + 1

    def run(self):
        socket = self._connect()
        finished_bool = MutableBoolean(False)
        communication_handler = ClientCommunicationHandler(socket)
        while not finished_bool.get_boolean():
            time.sleep(self.WAIT)
            query_result = communication_handler.get_query_results()
            query_result.print()
            finished_bool.set(query_result.final_result)

    def _connect(self):
        attempts = 0
        while attempts < self.MAX_ATTEMPTS:
            try:
                return Socket(self._host, self._port)
            except ConnectionRefusedError:
                time.sleep(self.DELAY_BETWEEN_ATTEMPTS)
                attempts += 1
        time.sleep(self.WAIT)
