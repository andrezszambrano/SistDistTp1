import logging

from .packet import Packet
from .queue_communication_handler import QueueCommunicationHandler
from .protocol import MONTREAL
from .rabb_prod_cons_queue import RabbProdConsQueue
from .rabb_publ_subs_queue import RabbPublSubsQueue

class YearsFilterer:
    def __init__(self, channel1, channel2):
        self._channel1 = channel1
        self._channel2 = channel2
        self._communication_receiver = QueueCommunicationHandler(None)

    def run(self):
        self.__recv_and_filter_station_data()
        self.__recv_and_filter_trips_data()

    def __recv_and_filter_station_data(self):
        self.__initialize_queues_to_recv_stations()
        self._station_queue.start_recv_loop()
        self._station_communication_handler.send_station_finished()
        self._channel1.close()
        logging.info(f"Finished receiving station data")

    def __filter_station_data(self, _ch, _method, _properties, body):
        station_batch = self._communication_receiver.recv_station_batch(Packet(body))
        if station_batch is None:
            self._channel1.stop_consuming()
            return
        filtered_stations = []
        for station in station_batch:
            if station.yearid in [2016, 2017]:
                filtered_stations.append(station)
        self._station_communication_handler.send_batch_to_station_processes(filtered_stations)

    def __initialize_queues_to_recv_stations(self):
        self._station_queue = RabbPublSubsQueue(self._channel1, "StationData", self.__filter_station_data)
        filtered_stations_queue = RabbPublSubsQueue(self._channel1, "2016-17Stations")
        self._station_communication_handler = QueueCommunicationHandler(filtered_stations_queue)

    def __recv_and_filter_trips_data(self):
        self.__initialize_queues_to_recv_and_send_trips()
        self._trip_queue.start_recv_loop()
        self._trips_communication_handler.send_finished()
        self._channel2.close()
        logging.info(f"Finished receiving trips data")

    def __filter_trip_data(self, _ch, _method, _properties, body):
        trip_batch = self._communication_receiver.recv_trip_batch(Packet(body))
        if trip_batch is None:
            self._channel2.stop_consuming()
            return
        filtered_trips = []
        for trip in trip_batch:
            year =  trip.start_date_time.date().year
            if year in [2016, 2017]:
                filtered_trips.append(trip)
        self._trips_communication_handler.send_trip_batch_to_processes(filtered_trips)

    def __initialize_queues_to_recv_and_send_trips(self):
        self._trip_queue = RabbPublSubsQueue(self._channel2, "TripData", self.__filter_trip_data)
        filtered_trips_queue = RabbPublSubsQueue(self._channel2, "2016-17Trips")
        self._trips_communication_handler = QueueCommunicationHandler(filtered_trips_queue)