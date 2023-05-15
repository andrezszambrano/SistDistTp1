import logging
import signal

from .client_communication_handler import ClientCommunicationHandler
from .socket_wrapper import Socket

WEATHER_DATA = "W"
WEATHER_FINISHED = "D"
STATION_FINISHED = "E"
STATION_DATA = "S"
TRIP_DATA = "T"
FINISHED = "F"

class Sender:
    def __init__(self, server_address):
        host, _port = server_address.split(':')
        port = int(_port)
        self._socket = Socket(host, port)
        self._keep_receiving = True

    def __exit_gracefully(self, _signum, _frame):
        self._keep_receiving = False

    def run(self, queue):
        signal.signal(signal.SIGTERM, self.__exit_gracefully)
        counter = 0
        weather_finished_counter = 0
        station_finished_counter = 0
        communication_handler = ClientCommunicationHandler(self._socket)
        while self._keep_receiving:
            data = queue.get()
            if data[0] == FINISHED:
                counter = counter + 1
                self._keep_receiving = not (counter == 3)
            elif data[0] == WEATHER_FINISHED:
                weather_finished_counter = weather_finished_counter + 1
                if weather_finished_counter == 3:
                    communication_handler.send_weather_finished()
            elif data[0] == STATION_FINISHED:
                station_finished_counter = station_finished_counter + 1
                if station_finished_counter == 3:
                    communication_handler.send_station_finished()
            elif data[0] == WEATHER_DATA:
                communication_handler.send_weather_batch(data[1])
            elif data[0] == STATION_DATA:
                communication_handler.send_station_batch(data[1])
            elif data[0] == TRIP_DATA:
                communication_handler.send_trip_batch(data[1])
        communication_handler.send_finished()
        self._socket.shutdown_and_close()
