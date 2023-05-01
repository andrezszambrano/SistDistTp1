import logging


class Trip2016_17Action():
    def __init__(self, station_occurrence_batch):
        self._station_occurrence_batch = station_occurrence_batch

    def perform_action__(self, _finished_bool, _counter, query_data, _query_communication_handler, printing_counter):
        #logging.debug(f"{query_results.year_to_station_to_counter}")|
        for station_occurrence in self._station_occurrence_batch:
            year = station_occurrence[0]
            city = station_occurrence[1]
            station_name = station_occurrence[2]
            city_n_station_dict = query_data.year_to_station_to_counter[year]
            key = (station_name, city)
            if key in city_n_station_dict:
                city_n_station_dict[key] = city_n_station_dict[key] + 1
            else:
                city_n_station_dict.update({key: 1})
            printing_counter.increase()
