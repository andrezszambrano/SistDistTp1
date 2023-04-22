import logging

from .action import Action


class FinishedAction(Action):
    def __init__(self):
        super(FinishedAction, self).__init__()

    def perform_action(self, finished_bool):
        finished_bool.set(True)
