import logging

from ..utils.running_average import RunningAverage


class RainyTripAction:
    def __init__(self, rainy_trip_duration_batch):
        self._rainy_trip_duration_batch = rainy_trip_duration_batch

    def perform_action__(self, _finished_bool, _counter, query_data, _query_communication_handler, printing_counter):
        date_to_avg_dict = query_data.date_to_duration_avg
        for rainy_trip_n_duration in self._rainy_trip_duration_batch:
            #logging.info(f"{rainy_trip_n_duration}")
            date = rainy_trip_n_duration[0]
            duration = rainy_trip_n_duration[1]
            if date in date_to_avg_dict:
                date_to_avg_dict[date].recalculate_avg(duration)
            else:
                date_to_avg_dict.update({date: RunningAverage(duration, 1)})
            printing_counter.increase()