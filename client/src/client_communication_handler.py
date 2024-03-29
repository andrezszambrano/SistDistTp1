import logging

from .client_protocol import ClientProtocol
from .packet import Packet


class ClientCommunicationHandler:
    def __init__(self, socket):
        self._socket = socket

    def send_station_batch(self, stations_list):
        packet = Packet()
        protocol = ClientProtocol()
        protocol.add_stations_batch_to_packet(packet, stations_list)
        self._socket.send(packet)

    def send_weather_batch(self, weathers_list):
        packet = Packet()
        protocol = ClientProtocol()
        protocol.add_weather_batch_to_packet(packet, weathers_list)
        self._socket.send(packet)

    def send_finished(self):
        protocol = ClientProtocol()
        packet = Packet()
        protocol.add_finished_to_packet(packet)
        self._socket.send(packet)

    def send_trip_batch(self, trips_list):
        packet = Packet()
        protocol = ClientProtocol()
        protocol.add_trip_batch_to_packet(packet, trips_list)
        self._socket.send(packet)

    def send_weather_finished(self):
        packet = Packet()
        protocol = ClientProtocol()
        protocol.add_weather_finished_to_packet(packet)
        self._socket.send(packet)

    def send_station_finished(self):
        packet = Packet()
        protocol = ClientProtocol()
        protocol.add_station_finished_to_packet(packet)
        self._socket.send(packet)

    def get_query_results(self):
        packet = Packet()
        protocol = ClientProtocol()
        protocol.add_query_ask_to_packet(packet)
        self._socket.send(packet)
        return protocol.recv_query_results(self._socket)
