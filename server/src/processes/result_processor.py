import logging

from ..communication_handlers.queue_communication_handler import QueueCommunicationHandler
from ..utils.running_average import RunningAverage


class ResultProcessor:
    def __init__(self, results_queue):
        self._results_queue = results_queue
        self._date_to_avg_dict = {}

    def run(self):
        result_communication_handler = QueueCommunicationHandler(self._results_queue)
        while True:
            tuple = result_communication_handler.recv_date_n_duration_or_finished()
            if tuple is None:
                break
            self._update_results(tuple[0], tuple[1])

        for date in self._date_to_avg_dict:
            if self._date_to_avg_dict[date].get_avg() > 0:
                logging.debug(f"{date}: {self._date_to_avg_dict[date].get_avg()}")

    def _update_results(self, date, duration):
        if date in self._date_to_avg_dict:
            self._date_to_avg_dict[date].recalculate_avg(duration)
        else:
            self._date_to_avg_dict.update({date: RunningAverage(duration, 1)})
