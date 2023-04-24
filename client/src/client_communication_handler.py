from .client_protocol import ClientProtocol
from .packet import Packet


class ClientCommunicationHandler:
    def __init__(self, socket):
        self._socket = socket

    def send_station_data(self, city_name, stations_list):
        packet = Packet()
        protocol = ClientProtocol()
        protocol.add_stations_chunk_to_packet(packet, city_name, stations_list)
        protocol.add_request_for_ack_to_packet(packet)
        self._socket.send(packet)
        protocol.recv_ack(self._socket)

    def send_weather_data(self, city_name, weathers_list):
        packet = Packet()
        protocol = ClientProtocol()
        protocol.add_weather_chunk_to_packet(packet, city_name, weathers_list)
        protocol.add_request_for_ack_to_packet(packet)
        self._socket.send(packet)
        protocol.recv_ack(self._socket)

    def send_finished(self):
        protocol = ClientProtocol()
        packet = Packet()
        protocol.add_finished_to_packet(packet)
        self._socket.send(packet)
