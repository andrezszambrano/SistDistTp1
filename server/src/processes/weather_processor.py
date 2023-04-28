from datetime import datetime
import logging

from ..communication_handlers.queue_communication_handler import QueueCommunicationHandler
from ..counter import Counter
from ..utils.running_average import RunningAverage


class WeatherProcessor:
    MIN_PRECTOT = 30

    def __init__(self, data_queue, trips_queue_n_id_tuple):
        self._data_queue = data_queue
        self._days_that_rained_in_city = set()
        self._date_to_avg_dict = {}
        self._trips_queue = trips_queue_n_id_tuple[0]
        self._trips_queue_id = trips_queue_n_id_tuple[1]

    def run(self):
        self._recv_weather_data()
        self._recv_trips_data()
        #final_dict = self._obtain_date_n_average_dict()
        for date in self._date_to_avg_dict:
            if self._date_to_avg_dict[date].get_avg() > 0:
                logging.debug(f"{date}: {self._date_to_avg_dict[date].get_avg()}")

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
        counter = Counter("WeatherProcess")
        while True:
            trip_data = trip_communication_handler.recv_trip_data()
            if trip_data is None:
                break
            self._process_trip(trip_data)
            counter.increase()

    def _process_trip(self, trip_data):
        #logging.debug(f"{key}")
        date =  trip_data.start_date_time.date()
        if (trip_data.city_name, date) in self._days_that_rained_in_city:
            if date in self._date_to_avg_dict:
                self._date_to_avg_dict[date].recalculate_avg(trip_data.duration_sec)
            else:
                self._date_to_avg_dict.update({date: RunningAverage(trip_data.duration_sec, 1)})
            #logging.debug(f"{trip_data.info()}")
            #self._days_that_rained_in_city[key].recalculate_avg(trip_data.duration_sec)

    def _obtain_date_n_average_dict(self):
        date_n_average = {}
        for city_n_date in self._days_that_rained_in_city:
            average = self._days_that_rained_in_city[city_n_date]
            date = city_n_date[1]
            if date in date_n_average:
                previous_average = date_n_average[date]
                date_n_average[date] = RunningAverage.join_running_averages(average, previous_average)
            else:
                date_n_average.update({date: average})
        return date_n_average
