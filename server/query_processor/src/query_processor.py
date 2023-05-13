import logging

from .packet import Packet
from .query_result import QueryResult
from .acceptor_socket import AcceptorSocket
from .queue_communication_handler import QueueCommunicationHandler
from .socket_communication_handler import SocketCommunicationHandler
from .rabb_prod_cons_queue import RabbProdConsQueue


class QueryProcessor:
    def __init__(self, port, channel):
        self._channel = channel
        ask_results_queue = RabbProdConsQueue(channel, "ResultData")
        self._ask_results_communication_handler = QueueCommunicationHandler(ask_results_queue)
        self._query_result_queue = RabbProdConsQueue(channel, "QueryData", self.__process_query_data)
        self._query_result_communication_handler = QueueCommunicationHandler(None)
        acceptor_socket = AcceptorSocket('', port, 5)
        socket = acceptor_socket.accept()
        self._client_communicator_handler = SocketCommunicationHandler(socket)

    def __process_query_data(self, _ch, _method, _properties, body):
        query_data = self._query_result_communication_handler.recv_query_data(Packet(body))
        query_result = self.__transform_query_data_in_result(query_data)
        self._client_communicator_handler.send_query_results(query_result)
        if query_result.final_result:
            self._channel.stop_consuming()
            return
        self._client_communicator_handler.recv_query_ask()
        self._ask_results_communication_handler.send_query_ask()

    def run(self):
        self._client_communicator_handler.recv_query_ask()
        self._ask_results_communication_handler.send_query_ask()
        self._query_result_queue.start_recv_loop()
        self._channel.close()

    def __transform_query_data_in_result(self, query_data):
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
