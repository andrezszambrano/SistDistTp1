from .mutable_boolean import MutableBoolean
from .communication_handler import CommunicationHandler


class DataDistributer:
    def __init__(self, queue):
        self._queue = queue

    def run(self):
        finished_bool = MutableBoolean(False)
        communication_handler = CommunicationHandler(self._queue)
        while True:
            action = communication_handler.recv_data_distributer_action()
            action.perform_action(finished_bool)
