import logging

from .packet import Packet
from .queue_communication_handler import QueueCommunicationHandler
from .rabb_prod_cons_queue import RabbProdConsQueue
from .rabb_publ_subs_queue import RabbPublSubsQueue
from .finalized_exception import FinalizedException


class DataDistributor:
    AMOUNT_OF_STATIONS_SUBS = 2
    AMOUNT_OF_TRIP_SUBS = 3
    DUPLICATED_STATIONS_QUEUE_ID = 0
    MONTREAL_QUEUE_ID = 1

    def __init__(self, channel):
        self._data_queue = RabbProdConsQueue(channel, "AllData", self.__process_data)
        self._weather_queue = RabbProdConsQueue(channel, "WeatherData")
        self._station_queue = RabbPublSubsQueue(channel, "StationData")
        self._trips_queue = RabbPublSubsQueue(channel, "TripData")

    def __process_data(self, _ch, _method, _properties, body):
        server_communication_handler = QueueCommunicationHandler(self._data_queue)
        weather_communication_handler = QueueCommunicationHandler(self._weather_queue)
        stations_communication_handler = QueueCommunicationHandler(self._station_queue)
        trips_communication_handler = QueueCommunicationHandler(self._trips_queue)
        action = server_communication_handler.recv_data_distributer_action(Packet(body))
        action.perform_action_(None, weather_communication_handler, stations_communication_handler,
                               trips_communication_handler)

    def run(self):
        try:
            self._data_queue.start_recv_loop()
        except FinalizedException:
            logging.info(f"Finished receiving all data")
