import logging
from multiprocessing import Process

from .communication_handlers.queue_communication_handler import QueueCommunicationHandler
from .mutable_boolean import MutableBoolean
from .queues.prod_cons_queue import ProdConsQueue
from .weather_processor import WeatherProcessor


class DataDistributer:
    def __init__(self, data_queue):
        self._data_queue = data_queue
        self._weather_queue = ProdConsQueue()

    def run(self):
        finished_bool = MutableBoolean(False)
        server_communication_handler = QueueCommunicationHandler(self._data_queue)
        weather_communication_handler = QueueCommunicationHandler(self._weather_queue)
        weather_processor = self.__create_and_run_weather_processor()
        while not finished_bool.get_boolean():
            action = server_communication_handler.recv_data_distributer_action()
            action.perform_action_(finished_bool, weather_communication_handler)
        weather_processor.join()

    def __create_and_run_weather_processor(self):
        weather_processor = WeatherProcessor(self._weather_queue)
        weather_processor_process = Process(target=weather_processor.run, args=(), daemon=False)
        weather_processor_process.start()
        return weather_processor_process
