import logging

from .packet import Packet
from .queue_communication_handler import QueueCommunicationHandler
from .finalized_exception import FinalizedException
from .rabb_prod_cons_queue import RabbProdConsQueue


class WeatherProcessor:
    MIN_PRECTOT = 30

    def __init__(self, channel):
        self._channel = channel
        self._days_that_rained_in_city = set()
        #self._trips_queue = trips_queue_n_id_tuple[0]
        #self._trips_queue_id = trips_queue_n_id_tuple[1]
        #self._results_monitor_queue = results_monitor_queue

    def run(self):
        self.__recv_weather_data()
        #self.__recv_and_filter_trips_data()

    def process_weather_data(self, _ch, _method, _properties, body):
        weather_communication_handler = QueueCommunicationHandler(None)
        weather_batch = weather_communication_handler.recv_weather_batch(Packet(body))
        logging.info(f"Here!")
        if weather_batch is None:
            raise FinalizedException()
        for weather in weather_batch:
            logging.info(f"{weather.info()}")
            if weather.prectot > self.MIN_PRECTOT:
                self._days_that_rained_in_city.add((weather.city_name, weather.date))

    def __recv_weather_data(self):
        try:
            self._weather_queue = RabbProdConsQueue(self._channel, "WeatherData", self.process_weather_data)
            self._weather_queue.start_recv_loop()
        except FinalizedException:
            pass

    def __recv_and_filter_trips_data(self):
        trip_communication_handler = QueueCommunicationHandler(self._trips_queue, self._trips_queue_id)
        result_communication_handler = QueueCommunicationHandler(self._results_monitor_queue)
        while True:
            trip_batch = trip_communication_handler.recv_trip_batch()
            if trip_batch is None:
                break
            self.__filter_trip_batch(trip_batch, result_communication_handler)
        result_communication_handler.send_finished()

    def __filter_trip_batch(self, trip_batch, result_communication_handler):
        #logging.debug(f"{key}")
        rainy_trips_duration_batch = []
        for trip in trip_batch:
            date =  trip.start_date_time.date()
            if (trip.city_name, date) in self._days_that_rained_in_city:
                rainy_trips_duration_batch.append((date, trip.duration_sec))
        if len(rainy_trips_duration_batch) > 0:
            result_communication_handler.send_rainy_trip_duration_batch(rainy_trips_duration_batch)
