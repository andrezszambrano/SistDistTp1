

class StationFinishedAction:
    def __init__(self):
        pass

    def perform_action(self, _finished_bool, _client_communicator_handler, distributor_communicator_handler):
        distributor_communicator_handler.send_station_finished_to_distributer()

    def perform_action_(self, _finished_bool, _processes_per_layer, _weather_communication_handler, stations_communication_handler,
                    _trips_communication_handler):
        stations_communication_handler.send_station_finished_to_distributer()
