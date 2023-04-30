
from .action import Action


class FinishedAction(Action):
    def __init__(self):
        super(FinishedAction, self).__init__()

    def perform_action(self, finished_bool, _client_communicator_handler, distributor_communicator_handler):
        finished_bool.set(True)
        distributor_communicator_handler.send_finished()

    def perform_action_(self, finished_bool, weather_communication_handler, stations_communication_handler,
                        trips_communication_handler):
        finished_bool.set(True)
        weather_communication_handler.send_finished()
        stations_communication_handler.send_finished()
        trips_communication_handler.send_finished()

    def perform_action__(self, finished_bool, counter, query_results, _query_communication_handler):
        counter.increase()
        if counter.get() == 2:
            finished_bool.set(True)
            query_results.set_final_data()
