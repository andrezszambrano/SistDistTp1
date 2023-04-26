import logging

from ..communication_handlers.queue_communication_handler import QueueCommunicationHandler


class WeatherProcessor:
    MIN_PRECTOT = 30

    def __init__(self, data_queue):
        self._data_queue = data_queue
        self._days_that_rained_in_city = set()

    def run(self):
        communication_handler = QueueCommunicationHandler(self._data_queue)
        while True:
            weather_data = communication_handler.recv_weather_data()
            if weather_data is None:
                break
            elif weather_data.prectot > self.MIN_PRECTOT:
                self._days_that_rained_in_city.add((weather_data.city_name, weather_data.date))
        logging.debug(f"Days that rained:{self._days_that_rained_in_city}")
        #for day in self._days_that_rained_in_city:
            #logging.debug(f"{day}")
