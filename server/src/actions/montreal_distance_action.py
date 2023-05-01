from ..utils.running_average import RunningAverage


class MontrealDistanceAction:
    def __init__(self, station_distance_occurrence_batch):
        self._station_distance_occurrence_batch = station_distance_occurrence_batch

    def perform_action__(self, _finished_bool, _counter, query_data, _query_communication_handler, printing_counter):
        for station_distance_occurrence in self._station_distance_occurrence_batch:
            year = station_distance_occurrence[0]
            station_name = station_distance_occurrence[1]
            distance = station_distance_occurrence[2]
            station_key = (year, station_name)
            station_to_distance_avg_dict = query_data.station_to_distance_avg
            if station_key in station_to_distance_avg_dict:
                station_to_distance_avg_dict[station_key].recalculate_avg(distance)
            else:
                station_to_distance_avg_dict.update({station_key: RunningAverage(distance, 1)})
        printing_counter.increase()
