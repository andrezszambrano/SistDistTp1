import logging

from .protocol import Protocol
from .query_result import QueryResult


class ClientProtocol(Protocol):

    def __init__(self):
        super(ClientProtocol, self).__init__()

    def add_stations_chunk_to_packet(self, packet, stations_list):
        for station in stations_list:
            super().add_station_to_packet(packet, station)

    def add_weather_chunk_to_packet(self, packet, weather_list):
        for weather in weather_list:
            super().add_weather_to_packet(packet, weather)

    def add_trip_chunk_to_packet(self, packet, trips_list):
        for trip in trips_list:
            super().add_trip_to_packet(packet, trip)

    def add_request_for_ack_to_packet(self, packet):
        packet.add_byte(super().ASK_ACK)

    def recv_ack(self, byte_stream):
        super()._recv_byte(byte_stream)

    def recv_query_results(self, byte_stream):
        rainy_date_n_avg_list = self.__recv_date_n_avg_list(byte_stream)
        station_that_doubled_list = self.__recv_station_that_doubled_list(byte_stream)
        far_away_station_list = self.__recv_far_away_station_list(byte_stream)
        final_query = super()._recv_boolean(byte_stream)
        return QueryResult(rainy_date_n_avg_list, station_that_doubled_list, far_away_station_list, final_query)

    def __recv_date_n_avg_list(self, byte_stream):
        byte = self._recv_byte(byte_stream)
        rainy_date_n_avg_list = []
        while byte != self.FINISHED:
            date = self._recv_date(byte_stream)
            duration_avg = self._recv_float(byte_stream)
            rainy_date_n_avg_list.append((date, duration_avg))
            byte = self._recv_byte(byte_stream)
        return rainy_date_n_avg_list

    def __recv_far_away_station_list(self, byte_stream):
        byte = self._recv_byte(byte_stream)
        rainy_date_n_avg_list = []
        while byte != self.FINISHED:
            station_name = self._recv_string(byte_stream)
            avg_distance = self._recv_float(byte_stream)
            rainy_date_n_avg_list.append((station_name, avg_distance))
            byte = self._recv_byte(byte_stream)
        return rainy_date_n_avg_list

    def __recv_station_that_doubled_list(self, byte_stream):
        byte = self._recv_byte(byte_stream)
        station_that_doubled_list = []
        while byte != self.FINISHED:
            station_name = self._recv_string(byte_stream)
            count2017 = self._recv_n_byte_number(byte_stream, self.FOUR_BYTES)
            count2016 = self._recv_n_byte_number(byte_stream, self.FOUR_BYTES)
            station_that_doubled_list.append((station_name, count2017, count2016))
            byte = self._recv_byte(byte_stream)
        return station_that_doubled_list
