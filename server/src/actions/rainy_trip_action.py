from ..utils.running_average import RunningAverage


class RainyTripAction:
    def __init__(self, date, duration_sec):
        self._date = date
        self._duration_sec = duration_sec

    def perform_action__(self, _finished_bool, _counter, query_results, _query_communication_handler):
        #query_results.update_date_to_avg_dict(self._date, self._duration_sec)
        date_to_avg_dict = query_results.date_to_duration_avg
        if self._date in date_to_avg_dict:
            date_to_avg_dict[self._date].recalculate_avg(self._duration_sec)
        else:
            date_to_avg_dict.update({self._date: RunningAverage(self._duration_sec, 1)})
