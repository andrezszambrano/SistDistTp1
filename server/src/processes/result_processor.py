import logging

from ..query_result import QueryResult
from ..communication_handlers.queue_communication_handler import QueueCommunicationHandler
from ..utils.mutable_boolean import MutableBoolean


class ResultProcessor:
    def __init__(self, results_queue, query_queue):
        self._results_queue = results_queue
        self._query_queue = query_queue
        self._query_results = QueryResult({}, False)

    def run(self):
        result_communication_handler = QueueCommunicationHandler(self._results_queue)
        query_communication_handler = QueueCommunicationHandler(self._query_queue)
        finished_bool = MutableBoolean(False)
        while not finished_bool.get_boolean():
            action = result_communication_handler.recv_results_processor_action()
            action.perform_action__(finished_bool, self._query_results, query_communication_handler)
        action = result_communication_handler.recv_results_processor_action()
        action.perform_action__(finished_bool, self._query_results, query_communication_handler)
