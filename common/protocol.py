import logging
from datetime import datetime, date
import struct

MONTREAL = "montreal"
WASHINGTON = "washington"
TORONTO = "toronto"

class Protocol:
    NO_FLOAT = 'N'
    FLOAT = 'F'
    WEATHER_DATA = 'W'
    STATION_DATA = 'S'
    TRIP_DATA = 'T'
    FINISHED = 'F'
    ASK_ACK = 'A'
    ACK = 'O'
    ASK_FOR_QUERY = 'Q'
    WEATHER_FINISHED = 'D'
    STATION_FINISHED = 'E'
    VALUE = 'V'
    FOUR_BYTES = 4
    TWO_BYTES = 2
    ONE_BYTE = 1

    def __init__(self):
        self._city_name_to_char = {MONTREAL: 'M', WASHINGTON: 'W', TORONTO: 'T'}

    def _recv_byte(self, byte_stream):
        return byte_stream.read(self.ONE_BYTE).decode('utf-8')

    def _recv_string(self, byte_stream):
        str_length = self._recv_n_byte_number(byte_stream, self.ONE_BYTE)
        return byte_stream.read(str_length).decode('utf-8')

    def _recv_n_byte_number(self, byte_stream, n):
        return int.from_bytes(byte_stream.read(n), byteorder='big')

    def _recv_date(self, byte_stream):
        date_len = self._recv_n_byte_number(byte_stream, self.ONE_BYTE)
        date_str = byte_stream.read(date_len).decode('utf-8')
        return date.fromisoformat(date_str)

    def _recv_date_time(self, byte_stream):
        date_time_len = self._recv_n_byte_number(byte_stream, self.ONE_BYTE)
        date_time_str = byte_stream.read(date_time_len).decode('utf-8')
        return datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')

    def _recv_boolean(self, byte_stream):
        i = self._recv_n_byte_number(byte_stream, self.ONE_BYTE)
        return True if i == 1 else False

    def _recv_float_else_none(self, byte_stream):
        aux = self._recv_byte(byte_stream)
        if aux == self.NO_FLOAT:
            return None
        else:
            return self._recv_float(byte_stream)

    def _recv_float(self, byte_stream):
        float_bytes = byte_stream.read(self.FOUR_BYTES)
        return struct.unpack('f', float_bytes)[0]

    def _add_float_else_none(self, packet, float_number):
        if float_number is None:
            packet.add_byte(self.NO_FLOAT)
        else:
            packet.add_byte(self.FLOAT)
            packet.add_float(float_number)

    def _add_station_to_packet(self, packet, station):
        packet.add_n_byte_number(self.TWO_BYTES, station.code)
        packet.add_string_and_length(station.name)
        self._add_float_else_none(packet, station.latitude)
        self._add_float_else_none(packet, station.longitude)
        packet.add_n_byte_number(self.TWO_BYTES, station.yearid)

    def _add_weather_to_packet(self, packet, weather, throw_unnecessary_data=False):
        #packet.add_byte(self._city_name_to_char[weather.city_name])
        packet.add_date(weather.date)
        self._add_float_else_none(packet, weather.prectot)
        if throw_unnecessary_data:
            for i in range(18):
                self._add_float_else_none(packet, None)
            return
        self._add_float_else_none(packet, weather.qv2m)
        self._add_float_else_none(packet, weather.rh2m)
        self._add_float_else_none(packet, weather.ps)
        self._add_float_else_none(packet, weather.t2m_range)
        self._add_float_else_none(packet, weather.ts)
        self._add_float_else_none(packet, weather.t2mdew)
        self._add_float_else_none(packet, weather.t2mwet)
        self._add_float_else_none(packet, weather.t2m_max)
        self._add_float_else_none(packet, weather.t2m_min)
        self._add_float_else_none(packet, weather.t2m)
        self._add_float_else_none(packet, weather.ws50m_range)
        self._add_float_else_none(packet, weather.ws10m_range)
        self._add_float_else_none(packet, weather.ws50m_min)
        self._add_float_else_none(packet, weather.ws10m_min)
        self._add_float_else_none(packet, weather.ws50m_max)
        self._add_float_else_none(packet, weather.ws10m_max)
        self._add_float_else_none(packet, weather.ws50m)
        self._add_float_else_none(packet, weather.ws10m)

    def add_weather_batch_to_packet(self, packet, weather_list, throw_unnecessary_data=False):
        packet.add_byte(self.WEATHER_DATA)
        packet.add_byte(self._city_name_to_char[weather_list[0].city_name])
        for weather in weather_list:
            packet.add_byte(self.VALUE)
            self._add_weather_to_packet(packet, weather, throw_unnecessary_data)
        packet.add_byte(self.FINISHED)

    def add_stations_batch_to_packet(self, packet, stations_list):
        packet.add_byte(self.STATION_DATA)
        packet.add_byte(self._city_name_to_char[stations_list[0].city_name])
        for station in stations_list:
            packet.add_byte(self.VALUE)
            self._add_station_to_packet(packet, station)
        packet.add_byte(self.FINISHED)

    def add_trip_batch_to_packet(self, packet, trip_list):
        packet.add_byte(self.TRIP_DATA)
        packet.add_byte(self._city_name_to_char[trip_list[0].city_name])
        for trip in trip_list:
            packet.add_byte(self.VALUE)
            self._add_trip_to_packet(packet, trip)
        packet.add_byte(self.FINISHED)

    def _add_trip_to_packet(self, packet, trip):
        packet.add_data_and_time(trip.start_date_time)
        packet.add_n_byte_number(self.TWO_BYTES, trip.start_station_code)
        packet.add_data_and_time(trip.end_date_time)
        packet.add_n_byte_number(self.TWO_BYTES, trip.end_station_code)
        packet.add_n_byte_number(self.FOUR_BYTES, trip.duration_sec)
        packet.add_boolean(trip.is_member)
        packet.add_n_byte_number(self.TWO_BYTES, trip.yearid)

    def add_finished_to_packet(self, packet):
        packet.add_byte(self.FINISHED)

    def add_weather_finished_to_packet(self, packet):
        packet.add_byte(self.WEATHER_FINISHED)

    def add_station_finished_to_packet(self, packet):
        packet.add_byte(self.STATION_FINISHED)

    def add_query_ask_to_packet(self, packet):
        packet.add_byte(self.ASK_FOR_QUERY)
