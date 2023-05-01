import logging

from ..query_result import QueryResult
from ..acceptor_socket import AcceptorSocket
from ..communication_handlers.queue_communication_handler import QueueCommunicationHandler
from ..communication_handlers.socket_communication_handler import SocketCommunicationHandler
from ..mutable_boolean import MutableBoolean


class QueryProcessor:
    def __init__(self, port, query_queue, results_queue):
        self._query_queue = query_queue
        self._results_queue = results_queue
        self._acceptor_socket = AcceptorSocket('', port + 1, 1)

    def run(self):
        socket = self._acceptor_socket.accept()
        client_communicator_handler = SocketCommunicationHandler(socket)
        query_communication_handler = QueueCommunicationHandler(self._query_queue)
        results_communication_handler = QueueCommunicationHandler(self._results_queue)
        finished_bool = MutableBoolean(False)
        while not finished_bool.get_boolean():
            client_communicator_handler.recv_query_ask()
            results_communication_handler.send_query_ask()
            query_data = query_communication_handler.recv_query_data()
            query_result = self.__process_query_data(query_data)
            client_communicator_handler.send_query_results(query_result)

    def __process_query_data(self, query_data):
        rainy_date_n_avg_list = self.__parse_date_to_duration_avg_dict_to_list(query_data.date_to_duration_avg)
        station_that_doubled_list = self.__parse_n_filter_year_to_station_to_counter_dict_to_list(query_data.year_to_station_to_counter)
        far_away_station_list = self.__parse_n_filter_station_to_distance_avg_dict_to_list(query_data.station_to_distance_avg)
        final_result = query_data.final_data
        return QueryResult(rainy_date_n_avg_list, station_that_doubled_list, far_away_station_list, final_result)

    def __parse_date_to_duration_avg_dict_to_list(self, date_to_duration_avg_dict):
        date_to_duration_avg_list = []
        for date, avg in iter(sorted(date_to_duration_avg_dict.items())):
            date_to_duration_avg_list.append((date, avg.get_avg()))
        return date_to_duration_avg_list

    def __parse_n_filter_year_to_station_to_counter_dict_to_list(self, year_to_station_to_counter_dict):
        year_to_station_to_counter_list = []
        city_n_station_2016_dict = year_to_station_to_counter_dict[2016]
        city_n_station_2017_dict = year_to_station_to_counter_dict[2017]
        for city_n_station, counter_2016 in iter(sorted(city_n_station_2016_dict.items())):
            if city_n_station in city_n_station_2017_dict:
                counter_2017 = city_n_station_2017_dict[city_n_station]
                if counter_2017 > 2 * counter_2016:
                    year_to_station_to_counter_list.append((city_n_station[1], counter_2017, counter_2016))
        return year_to_station_to_counter_list

    def __parse_n_filter_station_to_distance_avg_dict_to_list(self, station_to_distance_avg):
        far_away_station_list = []
        for station, avg in iter(sorted(station_to_distance_avg.items())):
            if avg.get_avg() >= 6:
                far_away_station_list.append((station, avg.get_avg()))
        return far_away_station_list
