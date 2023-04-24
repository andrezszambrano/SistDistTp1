import logging

from .communication_handlers.queue_communication_handler import QueueCommunicationHandler


class DuplicatedStationsProcessor:
    def __init__(self, data_queue):
        self._data_queue = data_queue
        self._stations = set()

    def run(self):
        communication_handler = QueueCommunicationHandler(self._data_queue)
        while True:
            station_data = communication_handler.recv_station_data()
            if station_data is None:
                break
            self._stations.add((station_data.city_name, station_data.code))
        logging.debug("Stations:")
        for station in self._stations:
            logging.debug(f"{station}")