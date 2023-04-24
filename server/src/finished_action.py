import logging

from .action import Action


class FinishedAction(Action):
    def __init__(self):
        super(FinishedAction, self).__init__()

    def perform_action(self, finished_bool, _client_communicator_handler, distributor_communicator_handler):
        finished_bool.set(True)
        distributor_communicator_handler.send_finished()

    def perform_action_(self, finished_bool):
        finished_bool.set(True)
