from .communication_handlers.queue_communication_handler import QueueCommunicationHandler
from .mutable_boolean import MutableBoolean


class DataDistributer:
    def __init__(self, queue):
        self._queue = queue

    def run(self):
        finished_bool = MutableBoolean(False)
        communication_handler = QueueCommunicationHandler(self._queue)
        while not finished_bool.get_boolean():
            action = communication_handler.recv_data_distributer_action()
            action.perform_action_(finished_bool)
