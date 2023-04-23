import logging

from .protocol import Protocol
from .packet import Packet

MONTREAL = "montreal"
WASHINGTON = "washington"
TORONTO = "toronto"

class ClientProtocol(Protocol):

    def __init__(self):
        super(ClientProtocol, self).__init__()
        self._city_name_to_char = {MONTREAL: 'M', WASHINGTON: 'W', TORONTO: 'T'}

    def send_weather_data(self, socket, city_name, weather_list):
        packet = Packet()
        for weather in weather_list:
            packet.add_byte(super().WEATHER_DATA)
            packet.add_byte(self._city_name_to_char[city_name])
            packet.add_date(weather.date)
            super()._add_float_else_none(packet, weather.prectot)
            super()._add_float_else_none(packet, weather.qv2m)
            super()._add_float_else_none(packet, weather.rh2m)
            super()._add_float_else_none(packet, weather.ps)
            super()._add_float_else_none(packet, weather.t2m_range)
            super()._add_float_else_none(packet, weather.ts)
            super()._add_float_else_none(packet, weather.t2mdew)
            super()._add_float_else_none(packet, weather.t2mwet)
            super()._add_float_else_none(packet, weather.t2m_max)
            super()._add_float_else_none(packet, weather.t2m_min)
            super()._add_float_else_none(packet, weather.t2m)
            super()._add_float_else_none(packet, weather.ws50m_range)
            super()._add_float_else_none(packet, weather.ws10m_range)
            super()._add_float_else_none(packet, weather.ws50m_min)
            super()._add_float_else_none(packet, weather.ws10m_min)
            super()._add_float_else_none(packet, weather.ws50m_max)
            super()._add_float_else_none(packet, weather.ws10m_max)
            super()._add_float_else_none(packet, weather.ws50m)
            super()._add_float_else_none(packet, weather.ws10m)
        packet.add_byte(super().ASK_ACK)
        packet.send_to_socket(socket)
        super()._recv_byte(socket)

    def send_station_data(self, socket, city_name, stations_list):
        packet = Packet()
        for station in stations_list:
            packet.add_byte(super().STATION_DATA)
            packet.add_byte(self._city_name_to_char[city_name])
            packet.add_n_byte_number(super().TWO_BYTES, station.code)
            packet.add_string_and_length(station.name)
            super()._add_float_else_none(packet, station.latitude)
            super()._add_float_else_none(packet, station.longitude)
            packet.add_n_byte_number(super().TWO_BYTES, station.yearid)
        packet.add_byte(super().ASK_ACK)
        packet.send_to_socket(socket)
        super()._recv_byte(socket)

    def send_finished(self, socket):
        packet = Packet()
        packet.add_byte(super().FINISHED)
        packet.send_to_socket(socket)
