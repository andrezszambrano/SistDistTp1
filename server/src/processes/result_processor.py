import logging

from ..counter import Counter
from ..query_result import QueryResult
from ..communication_handlers.queue_communication_handler import QueueCommunicationHandler
from ..mutable_boolean import MutableBoolean


class ResultMonitorProcessor:
    def __init__(self, results_monitor_queue, query_queue):
        self._results_monitor_queue = results_monitor_queue
        self._query_queue = query_queue
        self._query_results = QueryResult({}, {2016: {}, 2017: {}}, False)

    def run(self):
        result_monitor_communication_handler = QueueCommunicationHandler(self._results_monitor_queue)
        query_communication_handler = QueueCommunicationHandler(self._query_queue)
        finished_bool = MutableBoolean(False)
        counter = Counter()
        while not finished_bool.get_boolean():
            action = result_monitor_communication_handler.recv_results_processor_action()
            action.perform_action__(finished_bool, counter, self._query_results, query_communication_handler)
        action = result_monitor_communication_handler.recv_results_processor_action()
        action.perform_action__(finished_bool, counter, self._query_results, query_communication_handler)
