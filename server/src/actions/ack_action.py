from .action import Action


class AckAction(Action):

    def __init__(self):
        super(AckAction, self).__init__()

    def perform_action(self, _finished_bool, client_communicator_handler, _distributor_communicator_handler):
        client_communicator_handler.send_ack()
