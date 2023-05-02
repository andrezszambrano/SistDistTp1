import logging

from .packet import Packet
from .queue_communication_handler import QueueCommunicationHandler
from .finalized_exception import FinalizedException
from .rabb_prod_cons_queue import RabbProdConsQueue
from .rabb_publ_subs_queue import RabbPublSubsQueue


class DuplicatedStationsProcessor:
    def __init__(self, channel):
        self._station_queue = RabbPublSubsQueue(channel, "StationData", self.__process_station_data)
        self._trip_queue = RabbPublSubsQueue(channel, "TripData", self.__process_trip_data)
        self._communication_handler = QueueCommunicationHandler(None)
        result_queue = RabbProdConsQueue(channel, "ResultData")
        self._result_communication_handler = QueueCommunicationHandler(result_queue)
        self._stations = {}

    def run(self):
        self._recv_station_data()
        self._recv_and_filter_trips_data()

    def __process_station_data(self, _ch, _method, _properties, body):
        station_batch = self._communication_handler.recv_station_batch(Packet(body))
        if station_batch is None:
            raise FinalizedException
        for station in station_batch:
            if station.yearid in [2016, 2017]:
                self._stations.update({(station.city_name, station.yearid, station.code): station.name})

    def _recv_station_data(self):
        try:
            self._station_queue.start_recv_loop()
        except FinalizedException:
            pass

    def _recv_and_filter_trips_data(self):
        try:
            self._trip_queue.start_recv_loop()
        except FinalizedException:
            self._result_communication_handler.send_finished()

    def __process_trip_data(self, _ch, _method, _properties, body):
        trip_batch = self._communication_handler.recv_trip_batch(Packet(body))
        if trip_batch is None:
            raise FinalizedException
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
