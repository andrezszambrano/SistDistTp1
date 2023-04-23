import logging

from .client_protocol import ClientProtocol
from .socket_wrapper import Socket
from .packet import Packet

WEATHER_DATA = "W"
STATION_DATA = "S"
FINISHED = "F"

class Sender:
    def __init__(self, server_address):
        host, _port = server_address.split(':')
        port = int(_port)
        self._socket = Socket(host, port)

    def send_data(self, queue):
        counter = 0
        keep_receiving = True
        while keep_receiving:
            data = queue.get()
            if data[0] == FINISHED:
                counter = counter + 1
                keep_receiving = not (counter == 3)
            elif data[0] == WEATHER_DATA:
                self.__handle_weather_data(data[1], data[2])
            else:
                self.__handle_station_data(data[1], data[2])
        self.__send_finished_packet()
        self._socket.shutdown_and_close()

    def __handle_station_data(self, city_name, stations_list):
        packet = Packet()
        protocol = ClientProtocol()
        protocol.add_stations_chunk_to_packet(packet, city_name, stations_list)
        protocol.add_request_for_ack_to_packet(packet)
        self._socket.send(packet)
        self._socket.recv(1)

    def __handle_weather_data(self, city_name, weather_list):
        packet = Packet()
        protocol = ClientProtocol()
        protocol.add_weather_chunk_to_packet(packet, city_name, weather_list)
        protocol.add_request_for_ack_to_packet(packet)
        self._socket.send(packet)
        self._socket.recv(1)

    def __send_finished_packet(self):
        protocol = ClientProtocol()
        packet = Packet()
        protocol.add_finished_to_packet(packet)
        self._socket.send(packet)
