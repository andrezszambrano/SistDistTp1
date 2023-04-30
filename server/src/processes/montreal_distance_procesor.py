import logging

from haversine import haversine
from ..communication_handlers.queue_communication_handler import QueueCommunicationHandler
from ..protocol import MONTREAL


class MontrealDistanceProcessor:
    def __init__(self, stations_queue_n_id_tuple, trips_queue_n_id_tuple, results_monitor_queue):
        self._stations_queue = stations_queue_n_id_tuple[0]
        self._stations_queue_id = stations_queue_n_id_tuple[1]
        self._trips_queue = trips_queue_n_id_tuple[0]
        self._trips_queue_id = trips_queue_n_id_tuple[1]
        self._results_monitor_queue = results_monitor_queue
        self._stations = {}

    def run(self):
        self._recv_station_data()
        self._recv_and_filter_trips_data()

    def _recv_station_data(self):
        communication_handler = QueueCommunicationHandler(self._stations_queue, self._stations_queue_id)
        while True:
            station_data = communication_handler.recv_station_data()
            if station_data is None:
                break
            if station_data.city_name == MONTREAL:
                self._stations.update({(station_data.yearid, station_data.code): (station_data.name, station_data.latitude,
                                                                                  station_data.longitude)})

    def _recv_and_filter_trips_data(self):
        trip_communication_handler = QueueCommunicationHandler(self._trips_queue, self._trips_queue_id)
        result_communication_handler = QueueCommunicationHandler(self._results_monitor_queue)
        while True:
            trip_data = trip_communication_handler.recv_trip_data()
            if trip_data is None:
                break
            self._filter_trip(trip_data, result_communication_handler)
        result_communication_handler.send_finished()
    
    def _filter_trip(self, trip_data, result_communication_handler):
        if trip_data.city_name == MONTREAL:
            if (trip_data.yearid, trip_data.start_station_code) not in self._stations:
                return
            starting_station_data = self._stations[(trip_data.yearid, trip_data.start_station_code)]
            ending_station_data = self._stations[(trip_data.yearid, trip_data.end_station_code)]
            distance = self.__calculate_distance_betwee_stations(starting_station_data, ending_station_data)
            result_communication_handler.send_station_distance_occurence(trip_data.yearid, ending_station_data[0], distance)

    def __calculate_distance_betwee_stations(self, starting_station_data, ending_station_data):
        starting_latitude = starting_station_data[1]
        starting_longitude = starting_station_data[2]
        ending_latitude = ending_station_data[1]
        ending_longitude = ending_station_data[2]
        return haversine((starting_latitude, starting_longitude), (ending_latitude, ending_longitude))
