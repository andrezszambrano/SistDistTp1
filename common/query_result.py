import logging


class QueryResult:
    def __init__(self, rainy_date_n_avg_list, station_that_doubled_list, far_away_station_list, final_result):
        self.rainy_date_n_avg_list = rainy_date_n_avg_list
        self.station_that_doubled_list = station_that_doubled_list
        self.far_away_station_list = far_away_station_list
        self.final_result = final_result

    def set_final_result(self):
        self.final_result = True

    def print(self):
        if not self.final_result:
            return
        to_print_vec = [""]
        self.__append_final_or_partial_result(to_print_vec)
        self.__append_weather_query(to_print_vec)
        self.__append_duplicated_stations_query(to_print_vec)
        self.__append_far_away_stations_query(to_print_vec)
        to_print = "\n".join(to_print_vec)
        logging.info(f"{to_print}")

    def __append_final_or_partial_result(self, to_print_vec):
        if self.final_result:
            to_print_vec.append("FINAL RESULT")
        else:
            to_print_vec.append("PARTIAL RESULT")

    def __append_weather_query(self, to_print_vec):
        to_print_vec.append("\tQuery 1: Rainy trips average")
        if len(self.rainy_date_n_avg_list) == 0:
            to_print_vec.append("\t\tNo date average")
        else:
            for date_n_avg in self.rainy_date_n_avg_list:
                to_print_vec.append(f"\t\t{date_n_avg[0]}: {date_n_avg[1]}")

    def __append_duplicated_stations_query(self, to_print_vec):
        to_print_vec.append("\tQuery 2: Duplicated stations")
        if len(self.station_that_doubled_list) == 0:
            to_print_vec.append("\t\tNo duplicated stations")
        else:
            for station in self.station_that_doubled_list:
                to_print_vec.append(f"\t\tName: {station[0]}, 2017 counter: {station[1]}, 2016 counter: {station[2]}")

    def __append_far_away_stations_query(self, to_print_vec):
        to_print_vec.append("\tQuery 3: Far away stations")
        if len(self.far_away_station_list) == 0:
            to_print_vec.append("\t\tNo far away stations")
        else:
            for station_distance in self.far_away_station_list:
                to_print_vec.append(f"\t\tName: {station_distance[0]}, avg distance: {station_distance[1]}")
