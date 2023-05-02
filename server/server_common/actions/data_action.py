import logging

from ..protocol import Protocol
from .action import Action


class DataAction(Action):
    def __init__(self, data_type, data):
        super(DataAction, self).__init__()
        self._data_type = data_type
        self._data = data
        self._counter = 0

    def perform_action(self, _finished_bool, client_communicator_handler, distributor_communicator_handler):
        #logging.debug(f"{self._data_type}: {self._data.info()}")
        distributor_communicator_handler.send_data_to_distributer(self._data_type, self._data)

    def perform_action_(self, _finished_bool, weather_communication_handler, stations_communication_handler,
                        trips_communication_handler):
        #logging.debug(f"{self}: {self._data_type}")
        if self._data_type == Protocol().WEATHER_DATA:
            weather_communication_handler.send_batch_to_weather_process(self._data)
        elif self._data_type == Protocol().STATION_DATA:
            stations_communication_handler.send_batch_to_station_processes(self._data)
        else:
            trips_communication_handler.send_trip_batch_to_processes(self._data)