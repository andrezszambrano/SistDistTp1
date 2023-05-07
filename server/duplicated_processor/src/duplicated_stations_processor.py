import logging

from .packet import Packet
from .queue_communication_handler import QueueCommunicationHandler
from .rabb_prod_cons_queue import RabbProdConsQueue
from .rabb_publ_subs_queue import RabbPublSubsQueue


class DuplicatedStationsProcessor:
    def __init__(self, channel1, channel2):
        self._channel1 = channel1
        self._channel2 = channel2
        self._communication_handler = QueueCommunicationHandler(None)
        self._stations = {}

    def run(self):
        self._recv_station_data()
        self._recv_and_filter_trips_data()

    def __process_station_data(self, _ch, _method, _properties, body):
        station_batch = self._communication_handler.recv_station_batch(Packet(body))
        if station_batch is None:
            self._channel1.stop_consuming()
            return
        for station in station_batch:
            if station.yearid in [2016, 2017]:
                self._stations.update({(station.city_name, station.yearid, station.code): station.name})

    def _recv_station_data(self):
        self.__initialize_queues_to_recv_stations()
        self._station_queue.start_recv_loop()
        self._channel1.close()
        logging.info(f"Finished receiving station data")


    def _recv_and_filter_trips_data(self):
        self.__initialize_queues_to_recv_and_send_trips()
        self._trip_queue.start_recv_loop()
        self._result_communication_handler.send_finished()
        self._channel2.close()
        logging.info(f"Finished receiving trips data")

    def __process_trip_data(self, _ch, _method, _properties, body):
        trip_batch = self._communication_handler.recv_trip_batch(Packet(body))
        if trip_batch is None:
            self._channel2.stop_consuming()
            return
        self._filter_trip_batch(trip_batch)

    def _filter_trip_batch(self, trip_batch):
        trips_in_2016_or_2017 = []
        for trip in trip_batch:
            year =  trip.start_date_time.date().year
            if year in [2016, 2017]:
                station_key = (trip.city_name, year, trip.start_station_code)
                if station_key not in self._stations:
                    continue
                trips_in_2016_or_2017.append((year, trip.city_name, self._stations[station_key]))
        if len(trips_in_2016_or_2017) > 0:
            self._result_communication_handler.send_station_occurrence_batch(trips_in_2016_or_2017)

    def __initialize_queues_to_recv_stations(self):
        self._station_queue = RabbPublSubsQueue(self._channel1, "StationData", self.__process_station_data)

    def __initialize_queues_to_recv_and_send_trips(self):
        self._trip_queue = RabbPublSubsQueue(self._channel2, "TripData", self.__process_trip_data)
        self._result_queue = RabbProdConsQueue(self._channel2, "ResultData")
        self._result_communication_handler = QueueCommunicationHandler(self._result_queue)

