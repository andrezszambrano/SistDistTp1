import logging

from ..filter_protocol import FilterProtocol
from ..packet import Packet
from ..server_protocol import ServerProtocol


class QueueCommunicationHandler:
    def __init__(self, queue, queue_id=0):
        self._queue = queue
        self._queue_id = queue_id

    def send_finished(self):
        packet = Packet()
        protocol = ServerProtocol()
        protocol.add_finished_to_packet(packet)
        self._queue.send(packet)

    def send_data_to_distributer(self, data_type, data):
        packet = Packet()
        protocol = ServerProtocol()
        protocol.add_data_to_packet(packet, data_type, data)
        self._queue.send(packet)

    def send_weather_finished_to_distributer(self):
        packet = Packet()
        protocol = ServerProtocol()
        protocol.add_weather_finished_to_packet(packet)
        self._queue.send(packet)

    def send_station_finished_to_distributer(self):
        packet = Packet()
        protocol = ServerProtocol()
        protocol.add_station_finished_to_packet(packet)
        self._queue.send(packet)

    def send_batch_to_weather_process(self, weather_batch):
        packet = Packet()
        protocol = ServerProtocol()
        protocol.add_weather_batch_to_packet(packet, weather_batch, throw_unnecessary_data=True) #Todo eliminar esto
        self._queue.send(packet)

    def send_batch_to_station_processes(self, station_batch):
        packet = Packet()
        protocol = ServerProtocol()
        protocol.add_stations_batch_to_packet(packet, station_batch)
        self._queue.send(packet)

    def send_trip_batch_to_processes(self, trip_batch):
        packet = Packet()
        protocol = ServerProtocol()
        protocol.add_trip_batch_to_packet(packet, trip_batch)
        self._queue.send(packet)

    def send_query_ask(self):
        packet = Packet()
        protocol = ServerProtocol()
        protocol.add_query_ask_to_packet(packet)
        self._queue.send(packet)

    def send_query_data(self, query_data):
        packet = Packet()
        protocol = ServerProtocol()
        protocol.add_query_data_to_packet(packet, query_data)
        self._queue.send(packet)

    def send_station_occurrence_batch(self, trips_in_2016_or_2017):
        packet = Packet()
        protocol = FilterProtocol()
        protocol.add_station_occurrence_batch(packet, trips_in_2016_or_2017)
        self._queue.send(packet)

    def send_rainy_trip_duration_batch(self, rainy_trips_duration_batch):
        packet = Packet()
        protocol = FilterProtocol()
        protocol.add_rainy_trip_duration_batch(packet, rainy_trips_duration_batch)
        self._queue.send(packet)

    def send_station_distance_occurence(self, year, ending_station_name, distance):
        packet = Packet()
        protocol = FilterProtocol()
        protocol.add_station_name_distance_n_year(packet, year, ending_station_name, distance)
        self._queue.send(packet)

    def recv_data_distributer_action(self):
        protocol = ServerProtocol()
        packet = self._queue.get_packet(self._queue_id)
        return protocol.recv_data_distributer_action(packet)

    def recv_weather_batch(self):
        protocol = ServerProtocol()
        packet = self._queue.get_packet(self._queue_id)
        return protocol.recv_weather_batch_or_finished(packet)

    def recv_station_batch(self):
        protocol = ServerProtocol()
        packet = self._queue.get_packet(self._queue_id)
        return protocol.recv_station_batch_or_finished(packet)

    def recv_trip_batch(self):
        protocol = ServerProtocol()
        packet = self._queue.get_packet(self._queue_id)
        return protocol.recv_trip_batch_or_finished(packet)

    def recv_results_processor_action(self):
        protocol = FilterProtocol()
        packet = self._queue.get_packet(self._queue_id)
        return protocol.recv_results_processor_action(packet)

    def recv_query_data(self):
        protocol = ServerProtocol()
        packet = self._queue.get_packet(self._queue_id)
        return protocol.recv_query_data(packet)
