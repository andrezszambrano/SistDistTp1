import logging

from ..communication_handlers.queue_communication_handler import QueueCommunicationHandler
from ..printing_counter import PrintingCounter


class DuplicatedStationsProcessor:
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
        printing_counter = PrintingCounter("Stations", 1000)
        while True:
            station_batch = communication_handler.recv_station_data()
            if station_batch is None:
                break
            for station in station_batch:
                if station.yearid in [2016, 2017]:
                    self._stations.update({(station.city_name, station.yearid, station.code): station.name})
                printing_counter.increase()
        printing_counter.print_final()

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
        year =  trip_data.start_date_time.date().year
        if year in [2016, 2017]:
            station_key = (trip_data.city_name, year, trip_data.start_station_code)
            if station_key not in self._stations:
                return
            result_communication_handler.send_station_occurrence(year, trip_data.city_name, self._stations[station_key])
