import logging

from .action import Action
from .protocol import Protocol


class FinishedAction(Action):
    def __init__(self):
        super(FinishedAction, self).__init__()

    def perform_action(self, finished_bool, communication_handler):
        finished_bool.set(True)
        # queue.put(Protocol().FINISHED)