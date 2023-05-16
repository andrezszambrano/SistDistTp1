import logging
import signal

from .packet import Packet
from .queue_communication_handler import QueueCommunicationHandler
from .rabb_prod_cons_queue import RabbProdConsQueue
from .rabb_publ_subs_queue import RabbPublSubsQueue


class DuplicatedStationsProcessor:
    def __init__(self, channel1, channel2):
        self._channel1 = channel1
        self._channel2 = channel2
        self._communication_receiver = QueueCommunicationHandler(None)
        self._stations = {}
        self.__initialize_queues_to_recv_stations()
        self.__initialize_queues_to_recv_and_send_trips()
        signal.signal(signal.SIGTERM, self.__exit_gracefully)

    def __exit_gracefully(self, _signum, _frame):
        logging.info("Exiting gracefully")
        self._station_recv_communication_handler.close()
        self._trips_recv_communication_handler.close()
        self._result_sender_communication_handler.close()
        self._channel1.stop_consuming()
        self._channel1.close()
        self._channel2.stop_consuming()
        self._channel2.close()

    def run(self):
        self._recv_station_data()
        self._recv_and_filter_trips_data()

    def __process_station_data(self, _ch, _method, _properties, body):
        station_batch = self._communication_receiver.recv_station_batch(Packet(body))
        if station_batch is None:
            self._channel1.stop_consuming()
            return
        for station in station_batch:
            self._stations.update({(station.city_name, station.yearid, station.code): station.name})

    def _recv_station_data(self):
        self._station_recv_communication_handler.start_consuming()
        self._channel1.close()
        logging.info(f"Finished receiving station data")


    def _recv_and_filter_trips_data(self):
        self._trips_recv_communication_handler.start_consuming()
        self._result_sender_communication_handler.send_finished()
        self._channel2.close()
        logging.info(f"Finished receiving trips data")

    def __process_trip_data(self, _ch, _method, _properties, body):
        trip_batch = self._communication_receiver.recv_trip_batch(Packet(body))
        if type(trip_batch) is bool:
            self._channel2.stop_consuming()
            return
        self._filter_trip_batch(trip_batch)

    def _filter_trip_batch(self, trip_batch):
        trips_in_2016_or_2017 = []
        for trip in trip_batch:
            year =  trip.start_date_time.date().year
            station_key = (trip.city_name, year, trip.start_station_code)
            if station_key not in self._stations:
                continue
            trips_in_2016_or_2017.append((year, trip.city_name, self._stations[station_key]))
        self._result_sender_communication_handler.send_station_occurrence_batch(trips_in_2016_or_2017)

    def __initialize_queues_to_recv_stations(self):
        station_queue = RabbPublSubsQueue(self._channel1, "2016-17Stations", self.__process_station_data)
        self._station_recv_communication_handler = QueueCommunicationHandler(station_queue)

    def __initialize_queues_to_recv_and_send_trips(self):
        trips_queue = RabbPublSubsQueue(self._channel2, "2016-17Trips", self.__process_trip_data)
        self._trips_recv_communication_handler = QueueCommunicationHandler(trips_queue)
        self._result_queue = RabbProdConsQueue(self._channel2, "ResultData")
        self._result_sender_communication_handler = QueueCommunicationHandler(self._result_queue)
