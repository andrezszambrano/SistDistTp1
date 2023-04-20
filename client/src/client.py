import signal
from multiprocessing import Process, SimpleQueue

from .citys_data_reader import CityDataReader
from .sender import Sender

MONTREAL = "montreal"
WASHINGTON = "washington"
TORONTO = "toronto"

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
            city_reader = CityDataReader(city)
            city_readers_processes.append(Process(target=city_reader.run, args=(queue,), daemon=True).start())
        self._sender.send_data(queue)