import logging

from .client_protocol import ClientProtocol
from .socket_wrapper import Socket

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
        protocol = ClientProtocol()
        while keep_receiving:
            data = queue.get()
            if data[0] == FINISHED:
                counter = counter + 1
                keep_receiving = not (counter == 3)
            elif data[0] == WEATHER_DATA:
                pass
                #protocol.send_weather_data(self._socket, data[1], data[2])
                #break
                #logging.debug(f"{data[1]}{data[2][0].date} and {data[2][1].date}")
            else:
                #pass
                protocol.send_station_data(self._socket, data[1], data[2])
                #logging.debug(f"{data[1]}{data[2][0].name} and {data[2][1].name}")
        protocol.send_finished(self._socket)
        self._socket.shutdown_and_close()
