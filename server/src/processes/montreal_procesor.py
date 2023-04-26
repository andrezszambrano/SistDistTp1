import logging

from ..communication_handlers.queue_communication_handler import QueueCommunicationHandler
from ..protocol import MONTREAL


class MontrealProcessor:
    def __init__(self, data_queue, queue_id):
        self._data_queue = data_queue
        self._queue_id = queue_id
        self._stations = set()

    def run(self):
        communication_handler = QueueCommunicationHandler(self._data_queue, self._queue_id)
        while True:
            station_data = communication_handler.recv_station_data()
            if station_data is None:
                break
            if station_data.city_name == MONTREAL:
                self._stations.add((station_data.city_name, station_data.code))
        logging.debug(f"Montreal stations:{self._stations}")
        #for station in self._stations:
         #   logging.debug(f"{station}")