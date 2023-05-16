

class WeatherFinishedAction:
    def __init__(self):
        pass

    def perform_action(self, _finished_bool, _client_communicator_handler, distributor_communicator_handler):
        distributor_communicator_handler.send_weather_finished_to_distributer()

    def perform_action_(self, _finished_bool, _processes_per_layer, weather_communication_handler, _stations_communication_handler,
                    _trips_communication_handler):
        weather_communication_handler.send_weather_finished_to_distributer()
