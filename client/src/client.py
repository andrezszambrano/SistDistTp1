import logging
import signal
from multiprocessing import Process, SimpleQueue

from .citys_data_reader import CityDataReader
from .protocol import MONTREAL, WASHINGTON, TORONTO
from .sender import Sender

class Client:
    def __init__(self, server_address):
        # Initialize server socket
        self._sender = Sender(server_address)
        signal.signal(signal.SIGTERM, self.__exit_gracefully)

    def __exit_gracefully(self, signum, frame):
        pass

    def run(self):
        queue = SimpleQueue()
        cities = [MONTREAL, WASHINGTON, TORONTO]
        city_readers_processes = []
        for city in cities:
            city_reader = CityDataReader(city, queue)
            city_reader_process = Process(target=city_reader.run, args=(), daemon=True)
            city_reader_process.start()
            city_readers_processes.append(city_reader_process)
        self._sender.send_data(queue)
        for city_readers_process in city_readers_processes:
            city_readers_process.join()
        logging.debug(f"finished, all processes joined")
