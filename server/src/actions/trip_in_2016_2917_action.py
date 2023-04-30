import logging


class Trip2016_17Action():
    def __init__(self, city, year, station_name):
        self._city = city
        self._year = year
        self._station_name = station_name

    def perform_action__(self, _finished_bool, _counter, query_data, _query_communication_handler):
        #logging.debug(f"{query_results.year_to_station_to_counter}")
        city_n_station_dict = query_data.year_to_station_to_counter[self._year]
        key = (self._city, self._station_name)
        if key in city_n_station_dict:
            city_n_station_dict[key] = city_n_station_dict[key] + 1
        else:
            city_n_station_dict.update({key: 1})
