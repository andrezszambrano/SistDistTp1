import logging

from .actions.ack_action import AckAction
from .actions.data_action import DataAction
from .actions.finished_action import FinishedAction
from .actions.station_finished_action import StationFinishedAction
from .actions.weather_finished_action import WeatherFinishedAction
from .protocol import Protocol
from .query_data import QueryData
from .weather import Weather
from .station import Station
from .trip import Trip
from .average import Average


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
            weather_batch = self.__recv_weather_batch(byte_stream)
            return DataAction(super().WEATHER_DATA, weather_batch)
        elif message_type == super().STATION_DATA:
            station_batch = self.__recv_station_batch(byte_stream)
            #logging.debug(f"{station_batch}")
            return DataAction(super().STATION_DATA, station_batch)
        elif message_type == super().TRIP_DATA:
            trip_batch = self.__recv_trip_batch(byte_stream)
            return DataAction(super().TRIP_DATA, trip_batch)
        elif message_type == super().WEATHER_FINISHED:
            return WeatherFinishedAction()
        else:
            return StationFinishedAction()

    def __get_city_name(self, byte_stream):
        city_char = super()._recv_byte(byte_stream)
        return list(self._city_name_to_char.keys())[list(self._city_name_to_char.values()).index(city_char)]

    def add_data_to_packet(self, packet, data_type, data):
        if data_type == super().WEATHER_DATA:
            self.add_weather_batch_to_packet(packet, data)
        elif data_type == super().STATION_DATA:
            self.add_stations_batch_to_packet(packet, data)
        else:
            self.add_trip_batch_to_packet(packet, data)

    def recv_data_distributer_action(self, byte_stream):
        message_type = super()._recv_byte(byte_stream)
        if message_type == super().FINISHED:
            return FinishedAction()
        if message_type == super().WEATHER_DATA:
            weather_batch = self.__recv_weather_batch(byte_stream)
            return DataAction(super().WEATHER_DATA, weather_batch)
        elif message_type == super().STATION_DATA:
            station_batch = self.__recv_station_batch(byte_stream)
            return DataAction(super().STATION_DATA, station_batch)
        elif message_type == super().TRIP_DATA:
            trip_data = self.__recv_trip_batch(byte_stream)
            return DataAction(super().TRIP_DATA, trip_data)
        elif message_type == super().WEATHER_FINISHED:
            return WeatherFinishedAction()
        else:
            return StationFinishedAction()

    def recv_query_data(self, byte_stream):
        date_to_avg_dict = self.__recv_date_to_avg_dict(byte_stream)
        year_to_station_to_counter = self.__recv_year_to_station_to_counter(byte_stream)
        station_to_distance_avg = self.__recv_station_to_distance_avg(byte_stream)
        final_results = self._recv_boolean(byte_stream)
        return QueryData(date_to_avg_dict, year_to_station_to_counter, station_to_distance_avg, final_results)

    def __recv_date_to_avg_dict(self, byte_stream):
        byte = self._recv_byte(byte_stream)
        date_to_avg_dict = {}
        while byte != self.FINISHED:
            date = self._recv_date(byte_stream)
            duration_avg = self._recv_float(byte_stream)
            date_to_avg_dict.update({date: Average(duration_avg)})
            byte = self._recv_byte(byte_stream)
        return date_to_avg_dict

    def __recv_station_to_distance_avg(self, byte_stream):
        byte = self._recv_byte(byte_stream)
        station_to_distance_avg = {}
        while byte != self.FINISHED:
            station_name = self._recv_string(byte_stream)
            distance_avg = self._recv_float(byte_stream)
            station_to_distance_avg.update({(station_name): Average(distance_avg)})
            byte = self._recv_byte(byte_stream)
        return station_to_distance_avg

    def __recv_year_to_station_to_counter(self, byte_stream):
        year_to_station_to_counter = {}
        stations_2016 = self.__recv_stations_to_counter(byte_stream)
        year_to_station_to_counter.update({2016: stations_2016})
        stations_2017 = self.__recv_stations_to_counter(byte_stream)
        year_to_station_to_counter.update({2017: stations_2017})
        return year_to_station_to_counter

    def __recv_stations_to_counter(self, byte_stream):
        byte = self._recv_byte(byte_stream)
        city_n_stations_to_counter = {}
        while byte != self.FINISHED:
            city_name = self._recv_string(byte_stream)
            station_name = self._recv_string(byte_stream)
            count = self._recv_n_byte_number(byte_stream, self.FOUR_BYTES)
            city_n_stations_to_counter.update({(city_name, station_name): count})
            byte = self._recv_byte(byte_stream)
        return city_n_stations_to_counter

    def add_ack_to_packet(self, packet):
        packet.add_byte(super().ACK)

    def add_query_data_to_packet(self, packet, query_data):
        self.__add_date_to_avg_dict_to_packet(packet, query_data.date_to_duration_avg)
        self.__add_year_to_station_to_counter_dict_to_packet(packet, query_data.year_to_station_to_counter)
        self.__add_station_to_distance_avg_to_packet(packet, query_data.station_to_distance_avg)
        packet.add_boolean(query_data.final_data)

    def add_query_results_to_packet(self, packet, query_results):
        self.__add_rainy_date_n_avg_list(packet, query_results.rainy_date_n_avg_list)
        self.__add_station_that_doubled_list(packet, query_results.station_that_doubled_list)
        self.__add_far_away_station_list(packet, query_results.far_away_station_list)
        packet.add_boolean(query_results.final_result)

    def __add_rainy_date_n_avg_list(self, packet, rainy_date_n_avg_list):
        for date_n_avg in rainy_date_n_avg_list:
            packet.add_byte(super().VALUE)
            packet.add_date(date_n_avg[0])
            packet.add_float(date_n_avg[1])
        packet.add_byte(super().FINISHED)

    def __add_far_away_station_list(self, packet, far_away_station_list):
        for station_n_distance in far_away_station_list:
            packet.add_byte(super().VALUE)
            packet.add_string_and_length(station_n_distance[0])
            packet.add_float(station_n_distance[1])
        packet.add_byte(super().FINISHED)

    def __add_station_to_distance_avg_to_packet(self, packet, station_to_distance_avg):
        for station in station_to_distance_avg:
            packet.add_byte(super().VALUE)
            packet.add_string_and_length(station)
            packet.add_float(station_to_distance_avg[station].get_avg())
        packet.add_byte(super().FINISHED)

    def __add_station_that_doubled_list(self, packet, station_that_doubled_list):
        for station_tuple in station_that_doubled_list:
            packet.add_byte(super().VALUE)
            packet.add_string_and_length(station_tuple[0])
            packet.add_n_byte_number(super().FOUR_BYTES, station_tuple[1])
            packet.add_n_byte_number(super().FOUR_BYTES, station_tuple[2])
        packet.add_byte(super().FINISHED)

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
            packet.add_string_and_length(city_n_station[1])
            packet.add_string_and_length(city_n_station[0])
            packet.add_n_byte_number(super().FOUR_BYTES, city_n_station_to_counter[city_n_station])

    def recv_weather_batch_or_finished(self, byte_stream):
        message_type = super()._recv_byte(byte_stream)
        if message_type == super().WEATHER_FINISHED:
            return None
        we = self.__recv_weather_batch(byte_stream)
        return we

    def recv_station_batch_or_finished(self, byte_stream):
        message_type = super()._recv_byte(byte_stream)
        logging.info(f"{message_type}")
        if message_type == super().STATION_FINISHED:
            return None
        return self.__recv_station_batch(byte_stream)

    def recv_trip_batch_or_finished(self, byte_stream):
        message_type = super()._recv_byte(byte_stream)
        if message_type == super().FINISHED:
            return None
        return self.__recv_trip_batch(byte_stream)

    def recv_query_ask(self, byte_stream):
        return super()._recv_byte(byte_stream)

    def __recv_weather_data(self, byte_stream, city):
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

    def __recv_weather_batch(self, byte_stream):
        city = self.__get_city_name(byte_stream)
        weather_batch = []
        byte = super()._recv_byte(byte_stream)
        while byte != self.FINISHED:
            weather = self.__recv_weather_data(byte_stream, city)
            weather_batch.append(weather)
            byte = self._recv_byte(byte_stream)
        return weather_batch

    def __recv_station_batch(self, byte_stream):
        city = self.__get_city_name(byte_stream)
        station_batch = []
        byte = super()._recv_byte(byte_stream)
        while byte != self.FINISHED:
            station = self.__recv_station_data(byte_stream, city)
            station_batch.append(station)
            byte = self._recv_byte(byte_stream)
        return station_batch

    def __recv_trip_batch(self, byte_stream):
        city = self.__get_city_name(byte_stream)
        trip_batch = []
        byte = super()._recv_byte(byte_stream)
        while byte != self.FINISHED:
            trip = self.__recv_trip_data(byte_stream, city)
            trip_batch.append(trip)
            byte = self._recv_byte(byte_stream)
        return trip_batch

    def __recv_station_data(self, byte_stream, city):
        code = super()._recv_n_byte_number(byte_stream, super().TWO_BYTES)
        name = super()._recv_string(byte_stream)
        latitude = super()._recv_float_else_none(byte_stream)
        longitude = super()._recv_float_else_none(byte_stream)
        yearid = super()._recv_n_byte_number(byte_stream, super().TWO_BYTES)
        return Station(city, code, name, latitude, longitude, yearid)

    def __recv_trip_data(self, byte_stream, city):
        start_date_time = super()._recv_date_time(byte_stream)
        start_station_code = super()._recv_n_byte_number(byte_stream, super().TWO_BYTES)
        end_date_time = super()._recv_date_time(byte_stream)
        end_station_code = super()._recv_n_byte_number(byte_stream, super().TWO_BYTES)
        duration_sec = super()._recv_n_byte_number(byte_stream, super().FOUR_BYTES)
        is_member = super()._recv_boolean(byte_stream)
        yearid = super()._recv_n_byte_number(byte_stream, super().TWO_BYTES)
        return Trip(city, start_date_time, start_station_code, end_date_time, end_station_code, duration_sec, is_member,
                    yearid)

    def add_station_finished_to_packet(self, packet):
        packet.add_byte(super().STATION_FINISHED)
