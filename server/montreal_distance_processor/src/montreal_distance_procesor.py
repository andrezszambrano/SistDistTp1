import logging

from haversine import haversine

from .packet import Packet
from .queue_communication_handler import QueueCommunicationHandler
from .protocol import MONTREAL
from .rabb_prod_cons_queue import RabbProdConsQueue
from .rabb_publ_subs_queue import RabbPublSubsQueue


class MontrealDistanceProcessor:
    def __init__(self, channel1, channel2):
        self._channel1 = channel1
        self._channel2 = channel2
        self._communication_receiver = QueueCommunicationHandler(None)
        self._stations = {}

    def run(self):
        self._recv_station_data()
        self._recv_and_filter_trips_data()

    def __process_station_data(self, _ch, _method, _properties, body):
        station_batch = self._communication_receiver.recv_station_batch(Packet(body))
        if station_batch is None:
            self._channel1.stop_consuming()
            return
        for station in station_batch:
            if station.city_name == MONTREAL:
                self._stations.update({(station.yearid, station.code): (station.name, station.latitude,
                                                                        station.longitude)})
    def _recv_station_data(self):
        self.__initialize_queues_to_recv_stations()
        self._station_queue.start_recv_loop()
        self._channel1.close()
        logging.info(f"Finished receiving station data")

    def __process_trip_data(self, _ch, _method, _properties, body):
        trip_batch = self._communication_receiver.recv_trip_batch(Packet(body))
        if trip_batch is None:
            self._channel2.stop_consuming()
            return
        self._filter_trip_batch(trip_batch)

    def _recv_and_filter_trips_data(self):
        self.__initialize_queues_to_recv_and_send_trips()
        self._trip_queue.start_recv_loop()
        self._result_communication_handler.send_finished()
        self._channel2.close()
        logging.info(f"Finished receiving trips data")

    def _filter_trip_batch(self, trip_batch):
        station_distance_occurrence_batch = []
        for trip in trip_batch:
            if trip.city_name != MONTREAL:
                continue
            starting_key = (trip.yearid, trip.start_station_code)
            ending_key = (trip.yearid, trip.end_station_code)
            if (starting_key not in self._stations) or (ending_key not in self._stations):
                continue
            starting_station_data = self._stations[starting_key]
            ending_station_data = self._stations[ending_key]
            distance = self.__calculate_distance_betwee_stations(starting_station_data, ending_station_data)
            station_distance_occurrence_batch.append((trip.yearid, ending_station_data[0], distance))
        if len(station_distance_occurrence_batch) > 0:
            self._result_communication_handler.send_station_distance_occurrence_batch(station_distance_occurrence_batch)

    def __calculate_distance_betwee_stations(self, starting_station_data, ending_station_data):
        starting_latitude = starting_station_data[1]
        starting_longitude = starting_station_data[2]
        ending_latitude = ending_station_data[1]
        ending_longitude = ending_station_data[2]
        return haversine((starting_latitude, starting_longitude), (ending_latitude, ending_longitude))

    def __initialize_queues_to_recv_stations(self):
        self._station_queue = RabbPublSubsQueue(self._channel1, "StationData", self.__process_station_data)

    def __initialize_queues_to_recv_and_send_trips(self):
        self._trip_queue = RabbPublSubsQueue(self._channel2, "TripData", self.__process_trip_data)
        self._result_queue = RabbProdConsQueue(self._channel2, "ResultData")
        self._result_communication_handler = QueueCommunicationHandler(self._result_queue)

