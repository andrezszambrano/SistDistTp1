import logging


class QueryAskAction:
    def __init__(self):
        pass

    def perform_action__(self, _finished_bool, _counter, query_data, query_communication_handler, _printing_counter):
        query_communication_handler.send_query_data(query_data)
        