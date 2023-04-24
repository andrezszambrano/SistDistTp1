import logging
from .action import Action


class DataAction(Action):
    def __init__(self, data_type, city_name, data):
        super(DataAction, self).__init__()
        self._data_type = data_type
        self._city_name = city_name
        self._data = data

    def perform_action(self, _finished_bool, client_communicator_handler, distributor_communicator_handler):
        distributor_communicator_handler.send_data_to_distributer(self._data_type, self._city_name, self._data)
        #logging.debug(f"{self._data_type}, {self._city_name}: {self._data.info()}")

    def perform_action_(self, _finished_bool, weather_communication_handler):
        weather_communication_handler.send_data_to_weather_process(self._data_type, self._city_name, self._data)
        #logging.debug(f"{self._data_type}, {self._city_name}: {self._data.info()}")