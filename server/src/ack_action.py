from .action import Action


class AckAction(Action):

    def __init__(self):
        super(AckAction, self).__init__()

    def perform_action(self, _finished_bool, communication_handler):
        communication_handler.send_ack()
