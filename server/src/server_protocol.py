import logging

from .data_action import DataAction
from .finished_action import FinishedAction
from .protocol import Protocol
from .weather import Weather
from .station import Station


class ServerProtocol(Protocol):

    def __init__(self):
        super(ServerProtocol, self).__init__()

    def recv_action(self, socket):
        message_type = super()._recv_byte(socket)
        if message_type == super().FINISHED:
            return FinishedAction()
        city = super()._recv_byte(socket)
        if message_type == super().WEATHER_DATA:
            weather_data = self.__recv_weather_data(socket)
            return DataAction(self.WEATHER_DATA, city, weather_data)
        else:
            station_data = self.__recv_station_data(socket)
            return DataAction(self.STATION_DATA, city, station_data)

    def __recv_weather_data(self, socket):
        date = super()._recv_date(socket)
        prectot = super()._recv_float_else_none(socket)
        qv2m = super()._recv_float_else_none(socket)
        rh2m = super()._recv_float_else_none(socket)
        ps = super()._recv_float_else_none(socket)
        t2m_range = super()._recv_float_else_none(socket)
        ts = super()._recv_float_else_none(socket)
        t2mdew = super()._recv_float_else_none(socket)
        t2mwet = super()._recv_float_else_none(socket)
        t2m_max = super()._recv_float_else_none(socket)
        t2m_min = super()._recv_float_else_none(socket)
        t2m = super()._recv_float_else_none(socket)
        ws50m_range = super()._recv_float_else_none(socket)
        ws10m_range = super()._recv_float_else_none(socket)
        ws50m_min = super()._recv_float_else_none(socket)
        ws10m_min = super()._recv_float_else_none(socket)
        ws50m_max = super()._recv_float_else_none(socket)
        ws10m_max = super()._recv_float_else_none(socket)
        ws50m = super()._recv_float_else_none(socket)
        ws10m = super()._recv_float_else_none(socket)
        return Weather(date, prectot, qv2m, rh2m, ps, t2m_range, ts, t2mdew, t2mwet, t2m_max, t2m_min, t2m, ws50m_range,
                 ws10m_range, ws50m_min, ws10m_min, ws50m_max, ws10m_max, ws50m, ws10m)

    def __recv_station_data(self, socket):
        code = super()._recv_n_byte_number(socket, super().TWO_BYTES)
        name = super()._recv_string(socket)
        latitude = super()._recv_float_else_none(socket)
        longitude = super()._recv_float_else_none(socket)
        yearid = super()._recv_n_byte_number(socket, super().TWO_BYTES)
        return Station(code, name, latitude, longitude, yearid)