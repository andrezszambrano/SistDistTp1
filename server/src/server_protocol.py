import logging

from .actions.ack_action import AckAction
from .actions.data_action import DataAction
from .actions.finished_action import FinishedAction
from .actions.station_finished_action import StationFinishedAction
from .actions.weather_finished_action import WeatherFinishedAction
from .protocol import Protocol
from .weather import Weather
from .station import Station
from .trip import Trip


class ServerProtocol(Protocol):

    def __init__(self):
        super(ServerProtocol, self).__init__()

    def recv_action(self, byte_stream):
        message_type = super()._recv_byte(byte_stream)
        if message_type == super().FINISHED:
            return FinishedAction()
        elif message_type == super().ASK_ACK:
            return AckAction()
        if message_type == super().WEATHER_DATA:
            weather_data = self.__recv_weather_data(byte_stream)
            return DataAction(super().WEATHER_DATA, weather_data)
        elif message_type == super().STATION_DATA:
            station_data = self.__recv_station_data(byte_stream)
            return DataAction(super().STATION_DATA, station_data)
        elif message_type == super().TRIP_DATA:
            trip_data = self.__recv_trip_data(byte_stream)
            return DataAction(super().TRIP_DATA, trip_data)
        elif message_type == super().WEATHER_FINISHED:
            return WeatherFinishedAction()
        else:
            return StationFinishedAction()

    def __get_city_name(self, byte_stream):
        city_char = super()._recv_byte(byte_stream)
        return list(self._city_name_to_char.keys())[list(self._city_name_to_char.values()).index(city_char)]

    def add_data_to_packet(self, packet, data_type, data):
        if data_type == super().WEATHER_DATA:
            self.add_weather_to_packet(packet, data)
        elif data_type == super().STATION_DATA:
            self.add_station_to_packet(packet, data)
        else:
            self.add_trip_to_packet(packet, data)

    def recv_data_distributer_action(self, byte_stream):
        message_type = super()._recv_byte(byte_stream)
        if message_type == super().FINISHED:
            return FinishedAction()
        if message_type == super().WEATHER_DATA:
            weather_data = self.__recv_weather_data(byte_stream)
            return DataAction(super().WEATHER_DATA, weather_data)
        elif message_type == super().STATION_DATA:
            station_data = self.__recv_station_data(byte_stream)
            return DataAction(super().STATION_DATA, station_data)
        elif message_type == super().TRIP_DATA:
            trip_data = self.__recv_trip_data(byte_stream)
            return DataAction(super().TRIP_DATA, trip_data)
        elif message_type == super().WEATHER_FINISHED:
            return WeatherFinishedAction()
        else:
            return StationFinishedAction()

    def add_ack_to_packet(self, packet):
        packet.add_byte(super().ACK)

    def add_query_results_to_packet(self, packet, query_results):
        self.__add_date_to_avg_dict_to_packet(packet, query_results.date_to_duration_avg)
        self.__add_year_to_station_to_counter_dict_to_packet(packet, query_results.year_to_station_to_counter)
        packet.add_boolean(query_results.final_result)

    def __add_date_to_avg_dict_to_packet(self, packet, date_to_avg_dict):
        for date in date_to_avg_dict:
            packet.add_byte(super().VALUE)
            packet.add_date(date)
            packet.add_float(date_to_avg_dict[date].get_avg())
        packet.add_byte(super().FINISHED)

    def __add_year_to_station_to_counter_dict_to_packet(self, packet, year_to_station_to_counter):
        if 2016 in year_to_station_to_counter:
            self.__add_stations_n_counter_of_year_to_packet(packet, year_to_station_to_counter, 2016)
        packet.add_byte(super().FINISHED)
        if 2017 in year_to_station_to_counter:
            self.__add_stations_n_counter_of_year_to_packet(packet, year_to_station_to_counter, 2017)
        packet.add_byte(super().FINISHED)

    def __add_stations_n_counter_of_year_to_packet(self, packet, year_to_station_to_counter, year):
        city_n_station_to_counter = year_to_station_to_counter[year]
        for city_n_station in city_n_station_to_counter:
            packet.add_byte(super().VALUE)
            packet.add_string_and_length(city_n_station[0])
            packet.add_string_and_length(city_n_station[1])
            packet.add_n_byte_number(super().FOUR_BYTES, city_n_station_to_counter[city_n_station])

    def recv_weather_data_or_finished(self, byte_stream):
        message_type = super()._recv_byte(byte_stream)
        if message_type == super().WEATHER_FINISHED:
            return None
        return self.__recv_weather_data(byte_stream)

    def recv_station_data_or_finished(self, byte_stream):
        message_type = super()._recv_byte(byte_stream)
        if message_type == super().STATION_FINISHED:
            return None
        return self.__recv_station_data(byte_stream)

    def recv_trip_data_or_finished(self, byte_stream):
        message_type = super()._recv_byte(byte_stream)
        if message_type == super().FINISHED:
            return None
        return self.__recv_trip_data(byte_stream)

    def recv_query_ask(self, byte_stream):
        return super()._recv_byte(byte_stream)

    def __recv_weather_data(self, byte_stream):
        city = self.__get_city_name(byte_stream)
        date = super()._recv_date(byte_stream)
        prectot = super()._recv_float_else_none(byte_stream)
        qv2m = super()._recv_float_else_none(byte_stream)
        rh2m = super()._recv_float_else_none(byte_stream)
        ps = super()._recv_float_else_none(byte_stream)
        t2m_range = super()._recv_float_else_none(byte_stream)
        ts = super()._recv_float_else_none(byte_stream)
        t2mdew = super()._recv_float_else_none(byte_stream)
        t2mwet = super()._recv_float_else_none(byte_stream)
        t2m_max = super()._recv_float_else_none(byte_stream)
        t2m_min = super()._recv_float_else_none(byte_stream)
        t2m = super()._recv_float_else_none(byte_stream)
        ws50m_range = super()._recv_float_else_none(byte_stream)
        ws10m_range = super()._recv_float_else_none(byte_stream)
        ws50m_min = super()._recv_float_else_none(byte_stream)
        ws10m_min = super()._recv_float_else_none(byte_stream)
        ws50m_max = super()._recv_float_else_none(byte_stream)
        ws10m_max = super()._recv_float_else_none(byte_stream)
        ws50m = super()._recv_float_else_none(byte_stream)
        ws10m = super()._recv_float_else_none(byte_stream)
        return Weather(city, date, prectot, qv2m, rh2m, ps, t2m_range, ts, t2mdew, t2mwet, t2m_max, t2m_min, t2m, ws50m_range,
                       ws10m_range, ws50m_min, ws10m_min, ws50m_max, ws10m_max, ws50m, ws10m)

    def __recv_station_data(self, byte_stream):
        city = self.__get_city_name(byte_stream)
        code = super()._recv_n_byte_number(byte_stream, super().TWO_BYTES)
        name = super()._recv_string(byte_stream)
        latitude = super()._recv_float_else_none(byte_stream)
        longitude = super()._recv_float_else_none(byte_stream)
        yearid = super()._recv_n_byte_number(byte_stream, super().TWO_BYTES)
        return Station(city, code, name, latitude, longitude, yearid)

    def __recv_trip_data(self, byte_stream):
        city = self.__get_city_name(byte_stream)
        start_date_time = super()._recv_date_time(byte_stream)
        start_station_code = super()._recv_n_byte_number(byte_stream, super().TWO_BYTES)
        end_date_time = super()._recv_date_time(byte_stream)
        end_station_code = super()._recv_n_byte_number(byte_stream, super().TWO_BYTES)
        duration_sec = super()._recv_n_byte_number(byte_stream, super().FOUR_BYTES)
        is_member = super()._recv_boolean(byte_stream)
        yearid = super()._recv_n_byte_number(byte_stream, super().TWO_BYTES)
        return Trip(city, start_date_time, start_station_code, end_date_time, end_station_code, duration_sec, is_member,
                    yearid)
