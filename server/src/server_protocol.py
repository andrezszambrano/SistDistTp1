import logging

from .actions.ack_action import AckAction
from .actions.data_action import DataAction
from .actions.finished_action import FinishedAction
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
        else:
            trip_data = self.__recv_trip_data(byte_stream)
            return DataAction(super().TRIP_DATA, trip_data)

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
        else:
            trip_data = self.__recv_trip_data(byte_stream)
            return DataAction(super().TRIP_DATA, trip_data)

    def add_ack_to_packet(self, packet):
        packet.add_byte(super().ACK)

    def recv_weather_data_or_finished(self, byte_stream):
        message_type = super()._recv_byte(byte_stream)
        if message_type == super().FINISHED:
            return None
        return self.__recv_weather_data(byte_stream)

    def recv_station_data_or_finished(self, byte_stream):
        message_type = super()._recv_byte(byte_stream)
        if message_type == super().FINISHED:
            return None
        return self.__recv_station_data(byte_stream)

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
        logging.debug(f"Date: {start_date_time}")
        start_station_code = super()._recv_n_byte_number(byte_stream, super().TWO_BYTES)
        end_date_time = super()._recv_date_time(byte_stream)
        end_station_code = super()._recv_n_byte_number(byte_stream, super().TWO_BYTES)
        duration_sec = super()._recv_n_byte_number(byte_stream, super().FOUR_BYTES)
        is_member = super()._recv_boolean(byte_stream)
        yearid = super()._recv_n_byte_number(byte_stream, super().TWO_BYTES)
        return Trip(city, start_date_time, start_station_code, end_date_time, end_station_code, duration_sec, is_member,
                    yearid)