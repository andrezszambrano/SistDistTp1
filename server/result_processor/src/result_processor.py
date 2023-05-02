import logging

from .packet import Packet
from .printing_counter import PrintingCounter
from .query_data import QueryData
from .queue_communication_handler import QueueCommunicationHandler
from .rabb_prod_cons_queue import RabbProdConsQueue
from .finalized_exception import FinalizedException
from .counter import Counter


class ResultMonitorProcessor:
    def __init__(self, channel):
        self._results_monitor_queue = RabbProdConsQueue(channel, "ResultData", self.__process_result_data)
        self._result_monitor_communication_handler = QueueCommunicationHandler(None)
        self._printing_counter = PrintingCounter("Registered in result", 10000)
        self._counter = Counter()
        #self._query_queue = query_queue
        self._query_results = QueryData({}, {2016: {}, 2017: {}}, {}, False)

    def __process_result_data(self, _ch, _method, _properties, body):
        action = self._result_monitor_communication_handler.recv_results_processor_action(Packet(body))
        action.perform_action__(None, self._counter, self._query_results, None,
                                self._printing_counter)

    def run(self):
        #query_communication_handler = QueueCommunicationHandler(self._query_queue)
        try:
            self._results_monitor_queue.start_recv_loop()
        except FinalizedException:
            logging.info(f"Finished receiving weather data")

