import logging
import signal
import time

from .client_communication_handler import ClientCommunicationHandler
from .mutable_boolean import MutableBoolean
from .socket_wrapper import Socket


class QueryAsker:
    MAX_ATTEMPTS = 50
    DELAY_BETWEEN_ATTEMPTS = 4
    WAIT = 5

    def __init__(self, server_address):
        self._host, _port = server_address.split(':')
        self._port = int(_port)
        logging.info(f"{self._host}:{self._port}")
        self._finished_bool = MutableBoolean(False)

    def __exit_gracefully(self, _signum, _frame):
        self._finished_bool.set(True)

    def run(self):
        signal.signal(signal.SIGTERM, self.__exit_gracefully)
        socket = self._connect()
        communication_handler = ClientCommunicationHandler(socket)
        while not self._finished_bool.get_boolean():
            time.sleep(self.WAIT)
            query_result = communication_handler.get_query_results()
            query_result.print()
            self._finished_bool.set(query_result.final_result or self._finished_bool.get_boolean())
        socket.shutdown_and_close()

    def _connect(self):
        attempts = 0
        while attempts < self.MAX_ATTEMPTS:
            try:
                return Socket(self._host, self._port)
            except ConnectionRefusedError as e:
                time.sleep(self.DELAY_BETWEEN_ATTEMPTS)
                attempts += 1
