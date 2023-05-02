
from .action import Action
from .query_ask_action import QueryAskAction
from ..finalized_exception import FinalizedException


class FinishedAction(Action):
    def __init__(self):
        super(FinishedAction, self).__init__()

    def perform_action(self, finished_bool, _client_communicator_handler, distributor_communicator_handler):
        finished_bool.set(True)
        distributor_communicator_handler.send_finished()

    def perform_action_(self, _finished_bool, weather_communication_handler, stations_communication_handler,
                        trips_communication_handler):
        #finished_bool.set(True)
        weather_communication_handler.send_finished()
        stations_communication_handler.send_finished()
        trips_communication_handler.send_finished()
        raise FinalizedException()

    def perform_action__(self, _finished_bool, counter, query_results, _query_communication_handler, printing_counter):
        counter.increase()
        if counter.get() == 3:
            query_results.set_final_data()
            query_action = QueryAskAction()
            query_action.perform_action__(_finished_bool, counter, query_results, _query_communication_handler, printing_counter)
            printing_counter.print_final()
            raise FinalizedException()
        printing_counter.increase()
