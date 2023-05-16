import datetime
import logging
import signal

from .packet import Packet
from .queue_communication_handler import QueueCommunicationHandler
from .rabb_publ_subs_queue import RabbPublSubsQueue
from .rabb_prod_cons_queue import RabbProdConsQueue


class WeatherProcessor:
    MIN_PRECTOT = 30

    def __init__(self, instance_id, channel1, channel2):
        self._channel1 = channel1
        self._channel2 = channel2
        self._communication_receiver = QueueCommunicationHandler(None)
        self.__initialize_queues_to_recv_weather(instance_id)
        self.__initialize_queues_to_recv_and_send_trips()
        self._days_that_rained_in_city = set()
        signal.signal(signal.SIGTERM, self.__exit_gracefully)

    def __exit_gracefully(self, _signum, _frame):
        logging.info("Exiting gracefully")
        self._weather_recv_communication_handler.close()
        self._trips_recv_communication_handler.close()
        self._result_sender_communication_handler.close()
        self._channel1.stop_consuming()
        self._channel1.close()
        self._channel2.stop_consuming()
        self._channel2.close()

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
        self._weather_recv_communication_handler.start_consuming()
        self._channel1.close()
        logging.info(f"{len(self._days_that_rained_in_city)}, "
                     f"{('washington', datetime.date(2013, 6, 9)) in self._days_that_rained_in_city}")
        logging.info(f"Finished receiving weather data")

    def __process_trip_data(self, _ch, _method, _properties, body):
        trip_batch = self._communication_receiver.recv_trip_batch(Packet(body))
        if trip_batch is None:
            self._channel2.stop_consuming()
            return
        self.__filter_trip_batch(trip_batch)

    def __recv_and_filter_trips_data(self):
        self._trips_recv_communication_handler.start_consuming()
        self._result_sender_communication_handler.send_finished()
        self._channel2.close()
        logging.info(f"Finished receiving trips data")

    def __filter_trip_batch(self, trip_batch):
        rainy_trips_duration_batch = []
        for trip in trip_batch:
            date =  trip.start_date_time.date()
            if (trip.city_name, date) in self._days_that_rained_in_city:
                rainy_trips_duration_batch.append((date, trip.duration_sec))
        if len(rainy_trips_duration_batch) > 0:
            self._result_sender_communication_handler.send_rainy_trip_duration_batch(rainy_trips_duration_batch)

    def __initialize_queues_to_recv_weather(self, _instance_id):
        weather_queue = RabbPublSubsQueue(self._channel1, "WeatherData", self.__process_weather_data)
        #weather_queue = RabbProdConsQueue(self._channel1, "WeatherData", self.__process_weather_data)
        self._weather_recv_communication_handler = QueueCommunicationHandler(weather_queue)

    def __initialize_queues_to_recv_and_send_trips(self):
        trips_queue = RabbProdConsQueue(self._channel2, "TripDataQuery1", self.__process_trip_data)
        self._trips_recv_communication_handler = QueueCommunicationHandler(trips_queue)
        result_queue = RabbProdConsQueue(self._channel2, "ResultData")
        self._result_sender_communication_handler = QueueCommunicationHandler(result_queue)

