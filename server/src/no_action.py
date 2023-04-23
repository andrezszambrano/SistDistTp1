from .action import Action


class NoAction(Action):
    def __init__(self):
        super(NoAction, self).__init__()

    def perform_action(self, _finished_bool):
        pass
