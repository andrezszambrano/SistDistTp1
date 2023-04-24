from .mutable_boolean import MutableBoolean
from .communication_handler import CommunicationHandler


class DataDistributer:
    def __init__(self, queue):
        self._queue = queue

    def run(self):
        finished_bool = MutableBoolean(False)
        communication_handler = CommunicationHandler()
        while not finished_bool.get_boolean():
            action = communication_handler.recv_data_distributer_action(self._queue)
            action.perform_action_(finished_bool)
