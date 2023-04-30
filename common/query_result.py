import logging


class QueryResult:
    def __init__(self, date_to_duration_avg, year_to_station_to_counter, final_result):
        self.date_to_duration_avg = date_to_duration_avg
        self.year_to_station_to_counter = year_to_station_to_counter
        self.final_result = final_result

    def set_final_result(self):
        self.final_result = True

    def print(self):
        to_print_vec = [""]
        self.__append_final_or_partial_result(to_print_vec)
        self.__append_weather_query(to_print_vec)
        #self.__append_aux(to_print_vec)
        self.__append_duplicated_stations_query(to_print_vec)
        to_print = "\n".join(to_print_vec)
        logging.info(f"{to_print}")

    def __append_final_or_partial_result(self, to_print_vec):
        if self.final_result:
            to_print_vec.append("FINAL RESULT")
        else:
            to_print_vec.append("PARTIAL RESULT")

    def __append_weather_query(self, to_print_vec):
        to_print_vec.append("\tQuery 1: Rainy trips average")
        if not bool(self.date_to_duration_avg):
            to_print_vec.append("\t\tNo date average yet")
        else:
            for date in self.date_to_duration_avg:
                if self.date_to_duration_avg[date].get_avg() > 0:
                    to_print_vec.append(f"\t\t{date}: {self.date_to_duration_avg[date].get_avg()}")

    def __append_aux(self, to_print_vec):
        to_print_vec.append("\tQuery 2: Duplicated stations")
        to_print_vec.append(f"\t{self.year_to_station_to_counter}")

    def __append_duplicated_stations_query(self, to_print_vec):
        to_print_vec.append("\tQuery 2: Duplicated stations")
        to_append = []
        if not bool(self.year_to_station_to_counter):
            to_append.append("\t\tNo duplicated stations yet")
        else:
            city_n_station_2016_dict = self.year_to_station_to_counter[2016]
            city_n_station_2017_dict = self.year_to_station_to_counter[2017]
            for city_n_station in city_n_station_2016_dict:
                counter_2016 = city_n_station_2016_dict[city_n_station]
                if city_n_station in city_n_station_2017_dict:
                    counter_2017 = city_n_station_2017_dict[city_n_station]
                    if counter_2017 > 2 * counter_2016:
                        to_append.append(f"\t\tName: {city_n_station[1]}, 2017 counter: {counter_2017}, 2016 counter: {counter_2016}")
            if len(to_append) == 0:
                to_append.append("\t\tNo duplicated stations yet")
        to_print_vec.extend(to_append)
