import logging

from ..packet import Packet
from ..server_protocol import ServerProtocol


class QueueCommunicationHandler:
    def __init__(self, queue):
        self._queue = queue

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

    def send_data_to_weather_process(self, weather_data):
        packet = Packet()
        protocol = ServerProtocol()
        protocol.add_weather_to_packet(packet, weather_data, throw_unnecessary_data=True)
        self._queue.send(packet)

    def send_data_to_duplicated_station_process(self, station_data):
        packet = Packet()
        protocol = ServerProtocol()
        protocol.add_station_to_packet(packet, station_data)
        self._queue.send(packet)

    def recv_data_distributer_action(self):
        protocol = ServerProtocol()
        packet = self._queue.get_packet()
        return protocol.recv_data_distributer_action(packet)

    def recv_weather_data(self):
        protocol = ServerProtocol()
        packet = self._queue.get_packet()
        return protocol.recv_weather_data_or_finished(packet)

    def recv_station_data(self):
        protocol = ServerProtocol()
        packet = self._queue.get_packet()
        return protocol.recv_station_data_or_finished(packet)