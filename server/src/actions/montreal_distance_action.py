from ..utils.running_average import RunningAverage


class MontrealDistanceAction:
    def __init__(self, year, station_name, distance):
        self._year = year
        self._station_name = station_name
        self._distance = distance

    def perform_action__(self, _finished_bool, _counter, query_data, _query_communication_handler):
        station_key = (self._year, self._station_name)
        station_to_distance_avg_dict = query_data.station_to_distance_avg
        if station_key in station_to_distance_avg_dict:
            station_to_distance_avg_dict[station_key].recalculate_avg(self._distance)
        else:
            station_to_distance_avg_dict.update({station_key: RunningAverage(self._distance, 1)})
