import logging
import signal

from .mutable_boolean import MutableBoolean
from .packet import Packet
from .queue_communication_handler import QueueCommunicationHandler
from .rabb_prod_cons_queue import RabbProdConsQueue
from .rabb_publ_subs_queue import RabbPublSubsQueue
from .rabb_list_prod_cons_queue import RabbListProdConsQueue


class DataDistributor:
    AMOUNT_OF_STATIONS_SUBS = 2
    AMOUNT_OF_TRIP_SUBS = 3
    DUPLICATED_STATIONS_QUEUE_ID = 0
    MONTREAL_QUEUE_ID = 1

    def __init__(self, channel):
        self._channel = channel
        data_queue = RabbProdConsQueue(channel, "AllData", self.__process_data)
        weather_queue = RabbPublSubsQueue(channel, "WeatherData")
        station_queue = RabbPublSubsQueue(channel, "StationData")
        trips_queue = RabbListProdConsQueue(channel, ["TripDataQuery1", "TripDataQuery2", "TripDataQuery3"])
        self._finished_bool = MutableBoolean(False)
        self._server_communication_handler = QueueCommunicationHandler(data_queue)
        self._weather_communication_handler = QueueCommunicationHandler(weather_queue)
        self._stations_communication_handler = QueueCommunicationHandler(station_queue)
        self._trips_communication_handler = QueueCommunicationHandler(trips_queue)
        signal.signal(signal.SIGTERM, self.__exit_gracefully)

    def __exit_gracefully(self, _signum, _frame):
        logging.info("Exiting gracefully")
        self.__close_resources()

    def __process_data(self, _ch, _method, _properties, body):
        action = self._server_communication_handler.recv_data_distributer_action(Packet(body))
        action.perform_action_(self._finished_bool, self._weather_communication_handler,
                               self._stations_communication_handler, self._trips_communication_handler)
        if self._finished_bool.get_boolean():
            self._channel.stop_consuming()
            return

    def run(self):
        self._server_communication_handler.start_consuming()
        self.__close_resources()

    def __close_resources(self):
        self._server_communication_handler.close()
        self._weather_communication_handler.close()
        self._stations_communication_handler.close()
        self._trips_communication_handler.close()
        self._channel.stop_consuming()
        self._channel.close()
