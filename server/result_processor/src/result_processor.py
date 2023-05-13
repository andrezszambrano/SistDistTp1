import logging

from .mutable_boolean import MutableBoolean
from .packet import Packet
from .printing_counter import PrintingCounter
from .query_data import QueryData
from .queue_communication_handler import QueueCommunicationHandler
from .rabb_prod_cons_queue import RabbProdConsQueue
from .counter import Counter


class ResultMonitorProcessor:
    def __init__(self, channel):
        self._channel = channel
        self._results_monitor_queue = RabbProdConsQueue(channel, "ResultData", self.__process_result_data)
        self._result_monitor_communication_handler = QueueCommunicationHandler(None)
        self._printing_counter = PrintingCounter("Registered in result", 10000)
        self._counter = Counter()
        query_queue = RabbProdConsQueue(channel, "QueryData")
        self._query_communication_handler = QueueCommunicationHandler(query_queue)
        self._query_results = QueryData({}, {2016: {}, 2017: {}}, {}, False)

    def __process_result_data(self, _ch, _method, _properties, body):
        action = self._result_monitor_communication_handler.recv_results_processor_action(Packet(body))
        action.perform_action__(self._finished_boolean, self._counter, self._query_results, self._query_communication_handler,
                                self._printing_counter)
        if self._finished_boolean.get_boolean():
            self._channel.stop_consuming()

    def run(self):
        self._finished_boolean = MutableBoolean(False)
        self._results_monitor_queue.start_recv_loop()
        self._channel.close()
        logging.info(f"Finished receiving weather data")

