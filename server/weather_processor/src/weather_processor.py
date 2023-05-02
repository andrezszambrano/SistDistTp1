import logging

from .packet import Packet
from .queue_communication_handler import QueueCommunicationHandler
from .finalized_exception import FinalizedException
from .rabb_prod_cons_queue import RabbProdConsQueue
from .rabb_publ_subs_queue import RabbPublSubsQueue


class WeatherProcessor:
    MIN_PRECTOT = 30

    def __init__(self, channel):
        self._weather_queue = RabbProdConsQueue(channel, "WeatherData", self.__process_weather_data)
        self._trip_queue = RabbPublSubsQueue(channel, "TripData", self.__process_trip_data)
        self._result_queue = RabbProdConsQueue(channel, "ResultData")
        self._weather_communication_handler = QueueCommunicationHandler(None)
        self._result_communication_handler = QueueCommunicationHandler(self._result_queue)
        self._days_that_rained_in_city = set()

    def run(self):
        self.__recv_weather_data()
        self.__recv_and_filter_trips_data()

    def __process_weather_data(self, _ch, _method, _properties, body):
        weather_batch = self._weather_communication_handler.recv_weather_batch(Packet(body))
        if weather_batch is None:
            raise FinalizedException()
        for weather in weather_batch:
            #logging.info(f"{weather}")
            if weather.prectot > self.MIN_PRECTOT:
                self._days_that_rained_in_city.add((weather.city_name, weather.date))

    def __recv_weather_data(self):
        try:
            self._weather_queue.start_recv_loop()
        except FinalizedException:
            logging.info(f"Finished receiving weather data")

    def __process_trip_data(self, _ch, _method, _properties, body):
        trip_communication_handler = QueueCommunicationHandler(None)
        #result_communication_handler = QueueCommunicationHandler(self._results_monitor_queue)
        trip_batch = trip_communication_handler.recv_trip_batch(Packet(body))
        if trip_batch is None:
            raise FinalizedException()
        self.__filter_trip_batch(trip_batch)

    def __recv_and_filter_trips_data(self):
        try:
            self._trip_queue.start_recv_loop()
        except FinalizedException:
            self._result_communication_handler.send_finished()
            logging.info(f"Finished receiving weather data")

    def __filter_trip_batch(self, trip_batch):
        #logging.debug(f"{key}")
        rainy_trips_duration_batch = []
        for trip in trip_batch:
            #logging.info(f"{trip}")
            date =  trip.start_date_time.date()
            if (trip.city_name, date) in self._days_that_rained_in_city:
                rainy_trips_duration_batch.append((date, trip.duration_sec))
        if len(rainy_trips_duration_batch) > 0:
            self._result_communication_handler.send_rainy_trip_duration_batch(rainy_trips_duration_batch)
