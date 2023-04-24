import logging

from .client_protocol import ClientProtocol
from .communication_handler import CommunicationHandler
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
        communication_handler = CommunicationHandler(self._socket)
        while keep_receiving:
            data = queue.get()
            if data[0] == FINISHED:
                counter = counter + 1
                keep_receiving = not (counter == 3)
            elif data[0] == WEATHER_DATA:
                communication_handler.send_weather_data(data[1], data[2])
            else:
                communication_handler.send_station_data(data[1], data[2])
        communication_handler.send_finished()
        self._socket.shutdown_and_close()
