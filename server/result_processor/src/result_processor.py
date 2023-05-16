import logging
import signal

from .mutable_boolean import MutableBoolean
from .packet import Packet
from .printing_counter import PrintingCounter
from .query_data import QueryData
from .queue_communication_handler import QueueCommunicationHandler
from .rabb_prod_cons_queue import RabbProdConsQueue
from .counter import Counter


class ResultMonitorProcessor:
    QUERIES = 3

    def __init__(self, processes_per_layer, channel):
        self._channel = channel
        results_queue = RabbProdConsQueue(channel, "ResultData", self.__process_result_data)
        self._results_recv_communication_handler = QueueCommunicationHandler(results_queue)
        self._communication_handler = QueueCommunicationHandler(None)
        self._printing_counter = PrintingCounter("Registered in result", 10000)
        logging.info(f"{processes_per_layer}")
        self._counter = Counter(self.QUERIES * processes_per_layer)
        query_queue = RabbProdConsQueue(channel, "QueryData")
        self._query_communication_handler = QueueCommunicationHandler(query_queue)
        self._query_results = QueryData({}, {2016: {}, 2017: {}}, {}, False)
        self._finished_boolean = MutableBoolean(False)
        signal.signal(signal.SIGTERM, self.__exit_gracefully)

    def __exit_gracefully(self, _signum, _frame):
        logging.info("Exiting gracefully")
        self._results_recv_communication_handler.close()
        self._query_communication_handler.close()
        self._channel.stop_consuming()
        self._channel.close()

    def __process_result_data(self, _ch, _method, _properties, body):
        action = self._communication_handler.recv_results_processor_action(Packet(body))
        action.perform_action__(self._finished_boolean, self._counter, self._query_results, self._query_communication_handler,
                                self._printing_counter)
        if self._finished_boolean.get_boolean():
            self._channel.stop_consuming()

    def run(self):
        self._results_recv_communication_handler.start_consuming()
        self._channel.close()
        logging.info(f"Finished receiving results data")
