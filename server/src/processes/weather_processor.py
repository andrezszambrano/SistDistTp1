from datetime import datetime
import logging

from ..communication_handlers.queue_communication_handler import QueueCommunicationHandler
from ..counter import Counter
from ..printing_counter import PrintingCounter
from ..utils.running_average import RunningAverage


class WeatherProcessor:
    MIN_PRECTOT = 30

    def __init__(self, data_queue, trips_queue_n_id_tuple, results_monitor_queue):
        self._data_queue = data_queue
        self._days_that_rained_in_city = set()
        self._trips_queue = trips_queue_n_id_tuple[0]
        self._trips_queue_id = trips_queue_n_id_tuple[1]
        self._results_monitor_queue = results_monitor_queue

    def run(self):
        self._recv_weather_data()
        self._recv_and_filter_trips_data()

    def _recv_weather_data(self):
        weather_communication_handler = QueueCommunicationHandler(self._data_queue)
        #printing_counter = PrintingCounter("Weather", 1000)
        while True:
            weather_batch = weather_communication_handler.recv_weather_batch()
            if weather_batch is None:
                break
            for weather in weather_batch:
                if weather.prectot > self.MIN_PRECTOT:
                    self._days_that_rained_in_city.add((weather.city_name, weather.date))
                #printing_counter.increase()
        #printing_counter.print_final()
        #logging.debug(f"Days that rained:{self._days_that_rained_in_city}")

    def _recv_and_filter_trips_data(self):
        trip_communication_handler = QueueCommunicationHandler(self._trips_queue, self._trips_queue_id)
        result_communication_handler = QueueCommunicationHandler(self._results_monitor_queue)
        while True:
            trip_data = trip_communication_handler.recv_trip_data()
            if trip_data is None:
                break
            self._filter_trip(trip_data, result_communication_handler)
        result_communication_handler.send_finished()

    def _filter_trip(self, trip_data, result_communication_handler):
        #logging.debug(f"{key}")
        date =  trip_data.start_date_time.date()
        if (trip_data.city_name, date) in self._days_that_rained_in_city:
            result_communication_handler.send_rainy_trip_duration(date, trip_data.duration_sec)
