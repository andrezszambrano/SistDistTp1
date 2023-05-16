import logging
import signal

from .packet import Packet
from .queue_communication_handler import QueueCommunicationHandler
from .protocol import MONTREAL
from .rabb_publ_subs_queue import RabbPublSubsQueue
from .rabb_prod_cons_queue import RabbProdConsQueue

class MontrealFilterer:
    def __init__(self, instance_id, channel1, channel2):
        self._channel1 = channel1
        self._channel2 = channel2
        self._instance_id = instance_id
        self.__initialize_queues_to_recv_stations()
        self.__initialize_queues_to_recv_and_send_trips()
        self._communication_receiver = QueueCommunicationHandler(None)
        self._last_finished = False
        signal.signal(signal.SIGTERM, self.__exit_gracefully)

    def __exit_gracefully(self, _signum, _frame):
        logging.info("Exiting gracefully")
        self._station_sender_communication_handler.close()
        self._station_recv_communication_handler.close()
        self._trips_recv_communication_handler.close()
        self._trips_sender_communication_handler.close()
        self._channel1.stop_consuming()
        self._channel1.close()
        self._channel2.stop_consuming()
        self._channel2.close()

    def run(self):
        self.__recv_and_filter_station_data()
        self.__recv_and_filter_trips_data()

    def __recv_and_filter_station_data(self):
        self._station_recv_communication_handler.start_consuming()
        self._station_sender_communication_handler.send_station_finished()
        self._channel1.close()
        logging.info(f"Finished receiving station data")

    def __filter_station_data(self, _ch, _method, _properties, body):
        station_batch = self._communication_receiver.recv_station_batch(Packet(body))
        if station_batch is None:
            self._channel1.stop_consuming()
            return
        filtered_stations = []
        for station in station_batch:
            if station.city_name == MONTREAL:
                filtered_stations.append(station)
        self._station_sender_communication_handler.send_batch_to_station_processes(filtered_stations)

    def __initialize_queues_to_recv_stations(self):
        station_queue = RabbPublSubsQueue(self._channel1, "StationData", self.__filter_station_data)
        self._station_recv_communication_handler = QueueCommunicationHandler(station_queue)
        filtered_stations_queue = RabbPublSubsQueue(self._channel1, "MontrealStations")
        self._station_sender_communication_handler = QueueCommunicationHandler(filtered_stations_queue)

    def __recv_and_filter_trips_data(self):
        self._trips_recv_communication_handler.start_consuming()
        if self._last_finished:
            for _i in range(2): #number of processing duplicates
                self._trips_sender_communication_handler.send_finished()
        self._channel2.close()
        logging.info(f"Finished receiving trips data")

    def __filter_trip_data(self, _ch, _method, _properties, body):
        trip_batch = self._communication_receiver.recv_trip_batch(Packet(body))
        if type(trip_batch) is bool:
            last_finished = trip_batch
            self._channel2.stop_consuming()
            if last_finished:
                self._last_finished = True
            return
        filtered_trips = []
        for trip in trip_batch:
            if trip.city_name == MONTREAL:
                filtered_trips.append(trip)
        self._trips_sender_communication_handler.send_trip_batch_to_processes(filtered_trips)

    def __initialize_queues_to_recv_and_send_trips(self):
        trip_queue = RabbProdConsQueue(self._channel2, "TripDataQuery3", self.__filter_trip_data)
        self._trips_recv_communication_handler = QueueCommunicationHandler(trip_queue)
        filtered_trips_queue = RabbPublSubsQueue(self._channel2, "MontrealTrips")
        self._trips_sender_communication_handler = QueueCommunicationHandler(filtered_trips_queue)
