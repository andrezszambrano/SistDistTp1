from .client import MONTREAL, TORONTO, WASHINGTON
from .protocol import Protocol
from .packet import Packet


class ClientProtocol(Protocol):

    def __init__(self):
        super(ClientProtocol, self).__init__()
        self._city_name_to_char = {MONTREAL: 'M', WASHINGTON: 'W', TORONTO: 'T'}

    def send_weather_data(self, socket, city_name, weather_list):
        packet = Packet()
        for weather in weather_list:
            packet.add_byte(self._city_name_to_char[city_name])
            packet.add_date(weather.date)
            self._add_float_else_none(weather.prectot)
            self._add_float_else_none(weather.qv2m)
            self._add_float_else_none(weather.rh2m)
            self._add_float_else_none(weather.ps)
            self._add_float_else_none(weather.t2m_range)
            self._add_float_else_none(weather.ts)
            self._add_float_else_none(weather.t2mdew)
            self._add_float_else_none(weather.t2mwet)
            self._add_float_else_none(weather.t2m_max)
            self._add_float_else_none(weather.t2m_min)
            self._add_float_else_none(weather.t2m)
            self._add_float_else_none(weather.ws50m_range)
            self._add_float_else_none(weather.ws10m_range)
            self._add_float_else_none(weather.ws50m_min)
            self._add_float_else_none(weather.ws10m_min)
            self._add_float_else_none(weather.ws50m_max)
            self._add_float_else_none(weather.ws10m_max)
            self._add_float_else_none(weather.ws50m)
            self._add_float_else_none(weather.ws10m)
        packet.send_to_socket(socket)

    def __add_float_else_none(self, packet, float):
        if float is None:
            packet.add_byte(self.NO_FLOAT)
        else:
            packet.add_byte(self.FLOAT)
            packet.add_float(float)

    def send_station_data(self, socket, city_name, stations_list):
        packet = Packet()
        for station in stations_list:
            packet.add_byte(self._city_name_to_char[city_name])
            packet.add_n_byte_number(self.TWO_BYTES, station.code)
            packet.add_string_and_length(station.name)
            packet.__add_float_else_none(station.latitude)
            packet.__add_float_else_none(station.longitude)
            packet.add_n_byte_number(self.TWO_BYTES, station.yearid)
        packet.send_to_socket(socket)
