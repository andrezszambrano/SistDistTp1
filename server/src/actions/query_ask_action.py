

class QueryAskAction:
    def __init__(self):
        pass

    def perform_action__(self, _finished_bool, _counter, query_results, query_communication_handler):
        query_communication_handler.send_query_results(query_results)
        