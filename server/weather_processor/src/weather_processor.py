import logging

from .packet import Packet
from .queue_communication_handler import QueueCommunicationHandler
from .rabb_prod_cons_queue import RabbProdConsQueue
from .rabb_publ_subs_queue import RabbPublSubsQueue


class WeatherProcessor:
    MIN_PRECTOT = 30

    def __init__(self, channel1, channel2):
        self._channel1 = channel1
        self._channel2 = channel2
        self._communication_receiver = QueueCommunicationHandler(None)
        self._days_that_rained_in_city = set()

    def run(self):
        self.__recv_weather_data()
        self.__recv_and_filter_trips_data()

    def __process_weather_data(self, _ch, _method, _properties, body):
        weather_batch = self._communication_receiver.recv_weather_batch(Packet(body))
        if weather_batch is None:
            self._channel1.stop_consuming()
            return
        for weather in weather_batch:
            if weather.prectot > self.MIN_PRECTOT:
                self._days_that_rained_in_city.add((weather.city_name, weather.date))

    def __recv_weather_data(self):
        self.__initialize_queues_to_recv_weather()
        self._weather_queue.start_recv_loop()
        self._channel1.close()
        logging.info(f"Finished receiving weather data")

    def __process_trip_data(self, _ch, _method, _properties, body):
        trip_batch = self._communication_receiver.recv_trip_batch(Packet(body))
        if trip_batch is None:
            self._channel2.stop_consuming()
            return
        self.__filter_trip_batch(trip_batch)

    def __recv_and_filter_trips_data(self):
        self.__initialize_queues_to_recv_and_send_trips()
        self._trip_queue.start_recv_loop()
        self._result_communication_handler.send_finished()
        self._channel2.close()
        logging.info(f"Finished receiving trips data")

    def __filter_trip_batch(self, trip_batch):
        rainy_trips_duration_batch = []
        for trip in trip_batch:
            date =  trip.start_date_time.date()
            if (trip.city_name, date) in self._days_that_rained_in_city:
                rainy_trips_duration_batch.append((date, trip.duration_sec))
        if len(rainy_trips_duration_batch) > 0:
            self._result_communication_handler.send_rainy_trip_duration_batch(rainy_trips_duration_batch)

    def __initialize_queues_to_recv_weather(self):
        self._weather_queue = RabbProdConsQueue(self._channel1, "WeatherData", self.__process_weather_data)

    def __initialize_queues_to_recv_and_send_trips(self):
        self._trip_queue = RabbPublSubsQueue(self._channel2, "TripData", self.__process_trip_data)
        self._result_queue = RabbProdConsQueue(self._channel2, "ResultData")
        self._result_communication_handler = QueueCommunicationHandler(self._result_queue)

