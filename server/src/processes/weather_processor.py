import logging

from ..communication_handlers.queue_communication_handler import QueueCommunicationHandler


class WeatherProcessor:
    MIN_PRECTOT = 30

    def __init__(self, data_queue, trips_queue_n_id_tuple):
        self._data_queue = data_queue
        self._days_that_rained_in_city = set()
        self._trips_queue = trips_queue_n_id_tuple[0]
        self._trips_queue_id = trips_queue_n_id_tuple[1]

    def run(self):
        self._recv_weather_data()
        self._recv_trips_data()


    def _recv_weather_data(self):
        weather_communication_handler = QueueCommunicationHandler(self._data_queue)
        while True:
            weather_data = weather_communication_handler.recv_weather_data()
            if weather_data is None:
                break
            elif weather_data.prectot > self.MIN_PRECTOT:
                self._days_that_rained_in_city.add((weather_data.city_name, weather_data.date))
        #logging.debug(f"Days that rained:{self._days_that_rained_in_city}")

    def _recv_trips_data(self):
        trip_communication_handler = QueueCommunicationHandler(self._trips_queue, self._trips_queue_id)
        while True:
            trip_data = trip_communication_handler.recv_trip_data()
            if trip_data is None:
                break
            self._process_trip(trip_data)

    def _process_trip(self, trip_data):
        logging.debug(f"{trip_data.info()}")
