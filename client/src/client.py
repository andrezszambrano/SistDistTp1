import logging
import signal
from multiprocessing import Process, Queue

from .citys_data_reader import CityDataReader
from .protocol import MONTREAL, WASHINGTON, TORONTO
from .query_asker import QueryAsker
from .sender import Sender


class Client:
    def __init__(self, server_address, query_address):
        # Initialize server socket
        self._sender = Sender(server_address)
        self.query_asker = QueryAsker(query_address)

    def __exit_gracefully(self, _signum, _frame):
        logging.info("Exiting gracefully")
        self._query_asker_process.terminate()
        self._sender_process.terminate()
        for city_readers_process in self._city_readers_processes:
            city_readers_process.terminate()

    def run(self):
        queue = Queue()
        cities = [MONTREAL, WASHINGTON, TORONTO]
        self._city_readers_processes = []
        for city in cities:
            city_reader = CityDataReader(city, queue)
            city_reader_process = Process(target=city_reader.run, args=(), daemon=True)
            city_reader_process.start()
            self._city_readers_processes.append(city_reader_process)
        self._query_asker_process = self.__create_and_run_query_asker()
        self._sender_process = self.__create_and_run_server_process(queue)
        signal.signal(signal.SIGTERM, self.__exit_gracefully)
        for city_readers_process in self._city_readers_processes:
            city_readers_process.join()
        self._sender_process.join()
        self._query_asker_process.join()
        queue.close()
        logging.debug(f"finished, all processes joined")

    def __create_and_run_query_asker(self):
        query_asker_process = Process(target=self.query_asker.run, args=(), daemon=True)
        query_asker_process.start()
        return query_asker_process

    def __create_and_run_server_process(self, queue):
        sender_process = Process(target=self._sender.run, args=(queue,), daemon=True)
        sender_process.start()
        return sender_process
