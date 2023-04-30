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

    def send_data_to_weather_process(self, weather_data):
        packet = Packet()
        protocol = ServerProtocol()
        protocol.add_weather_to_packet(packet, weather_data, throw_unnecessary_data=True)
        self._queue.send(packet)

    def send_data_to_station_processes(self, station_data):
        packet = Packet()
        protocol = ServerProtocol()
        protocol.add_station_to_packet(packet, station_data)
        self._queue.send(packet)

    def send_trip_data_to_processes(self, trip_data):
        packet = Packet()
        protocol = ServerProtocol()
        protocol.add_trip_to_packet(packet, trip_data)
        self._queue.send(packet)

    def send_rainy_trip_duration(self, date, duration_sec):
        packet = Packet()
        protocol = FilterProtocol()
        protocol.add_date_n_duration(packet, date, duration_sec)
        self._queue.send(packet)

    def send_query_ask(self):
        packet = Packet()
        protocol = ServerProtocol()
        protocol.add_query_ask_to_packet(packet)
        self._queue.send(packet)

    def send_query_results(self, query_results):
        packet = Packet()
        protocol = ServerProtocol()
        protocol.add_query_results_to_packet(packet, query_results)
        self._queue.send(packet)

    def send_station_occurrence(self, year, city_name, station_name):
        packet = Packet()
        protocol = FilterProtocol()
        protocol.add_year_city_n_station_name_to_packet(packet, year, city_name, station_name)
        self._queue.send(packet)

    def recv_data_distributer_action(self):
        protocol = ServerProtocol()
        packet = self._queue.get_packet(self._queue_id)
        return protocol.recv_data_distributer_action(packet)

    def recv_weather_data(self):
        protocol = ServerProtocol()
        packet = self._queue.get_packet(self._queue_id)
        return protocol.recv_weather_data_or_finished(packet)

    def recv_station_data(self):
        protocol = ServerProtocol()
        packet = self._queue.get_packet(self._queue_id)
        return protocol.recv_station_data_or_finished(packet)

    def recv_trip_data(self):
        protocol = ServerProtocol()
        packet = self._queue.get_packet(self._queue_id)
        return protocol.recv_trip_data_or_finished(packet)

    def recv_results_processor_action(self):
        protocol = FilterProtocol()
        packet = self._queue.get_packet(self._queue_id)
        return protocol.recv_results_processor_action(packet)

    def recv_query_results(self):
        protocol = ServerProtocol()
        packet = self._queue.get_packet(self._queue_id)
        return protocol.recv_query_results(packet)
