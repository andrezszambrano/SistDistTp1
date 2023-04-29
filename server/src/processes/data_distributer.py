import logging
from multiprocessing import Process

from .result_processor import ResultProcessor
from ..communication_handlers.queue_communication_handler import QueueCommunicationHandler
from .duplicated_stations_processor import DuplicatedStationsProcessor
from .montreal_procesor import MontrealProcessor
from ..utils.mutable_boolean import MutableBoolean
from ..queues.prod_cons_queue import ProdConsQueue
from ..queues.publ_subs_queue import PublSubsQueue
from .weather_processor import WeatherProcessor


class DataDistributer:
    AMOUNT_OF_STATIONS_SUBS = 2
    DUPLICATED_STATIONS_QUEUE_ID = 0
    MONTREAL_QUEUE_ID = 1

    def __init__(self, data_queue):
        self._data_queue = data_queue
        self._weather_queue = ProdConsQueue()
        self._stations_queue = PublSubsQueue(self.AMOUNT_OF_STATIONS_SUBS)
        self._trips_queue = PublSubsQueue(self.AMOUNT_OF_STATIONS_SUBS)
        self._results_queue = ProdConsQueue()

    def run(self):
        finished_bool = MutableBoolean(False)
        server_communication_handler = QueueCommunicationHandler(self._data_queue)
        weather_communication_handler = QueueCommunicationHandler(self._weather_queue)
        stations_communication_handler = QueueCommunicationHandler(self._stations_queue)
        trips_communication_handler = QueueCommunicationHandler(self._trips_queue)

        weather_processor = self.__create_and_run_weather_processor()
        result_processor = self.__create_and_run_results_processor()
        #duplicated_stations_processor = self.__create_and_run_duplicated_stations_processor()
        #montreal_processor = self.__create_and_run_montreal_processor()
        while not finished_bool.get_boolean():
            action = server_communication_handler.recv_data_distributer_action()
            action.perform_action_(finished_bool, weather_communication_handler, stations_communication_handler,
                                   trips_communication_handler)
        weather_processor.join()
        result_processor.join()
        #duplicated_stations_processor.join()
        #montreal_processor.join()

    def __create_and_run_weather_processor(self):
        weather_processor = WeatherProcessor(self._weather_queue, (self._trips_queue, 0), self._results_queue)
        weather_processor_process = Process(target=weather_processor.run, args=(), daemon=False)
        weather_processor_process.start()
        return weather_processor_process

    def __create_and_run_duplicated_stations_processor(self):
        duplicated_stations_processor = DuplicatedStationsProcessor(self._stations_queue, self.DUPLICATED_STATIONS_QUEUE_ID)
        duplicated_stations_processor_process = Process(target=duplicated_stations_processor.run, args=(), daemon=False)
        duplicated_stations_processor_process.start()
        return duplicated_stations_processor_process

    def __create_and_run_montreal_processor(self):
        montreal_processor = MontrealProcessor(self._stations_queue, self.MONTREAL_QUEUE_ID)
        montreal_processor_process = Process(target=montreal_processor.run, args=(), daemon=False)
        montreal_processor_process.start()
        return montreal_processor_process

    def __create_and_run_results_processor(self):
        result_processor = ResultProcessor(self._results_queue)
        result_processor_process = Process(target=result_processor.run, args=(), daemon=False)
        result_processor_process.start()
        return result_processor_process

