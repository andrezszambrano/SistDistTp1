
from .action import Action
from .query_ask_action import QueryAskAction


class FinishedAction(Action):
    def __init__(self):
        super(FinishedAction, self).__init__()

    def perform_action(self, finished_bool, _client_communicator_handler, distributor_communicator_handler):
        finished_bool.set(True)
        distributor_communicator_handler.send_finished()

    def perform_action_(self, finished_bool, processes_per_layer, weather_communication_handler, stations_communication_handler,
                        trips_communication_handler):
        finished_bool.set(True)
        weather_communication_handler.send_finished()
        stations_communication_handler.send_finished()
        for _i in range(processes_per_layer - 1): #Amount of filterers - 1
            trips_communication_handler.send_finished()
        trips_communication_handler.send_last_finished()

    def perform_action__(self, finished_bool, counter, query_results, _query_communication_handler, printing_counter):
        finished = counter.increase()
        if finished:
            query_results.set_final_data()
            query_action = QueryAskAction()
            query_action.perform_action__(finished_bool, counter, query_results, _query_communication_handler, printing_counter)
            printing_counter.print_final()
            finished_bool.set(True)
        printing_counter.increase()
