import logging

from .actions.finished_action import FinishedAction
from .actions.montreal_distance_action import MontrealDistanceAction
from .actions.query_ask_action import QueryAskAction
from .actions.rainy_trip_action import RainyTripAction
from .actions.trip_in_2016_2917_action import Trip2016_17Action
from .protocol import Protocol


class FilterProtocol(Protocol):
    DATE_N_DURATION = 'P'
    STATION_OCCURRENCE = 'S'
    DISTANCE_OCCURRENCE = 'D'

    def __init__(self):
        super(FilterProtocol, self).__init__()

    def __add_date_n_duration(self, packet, date, duration_sec):
        packet.add_date(date)
        packet.add_n_byte_number(super().FOUR_BYTES, duration_sec)

    def add_rainy_trip_duration_batch(self, packet, rainy_trips_duration_batch):
        packet.add_byte(self.DATE_N_DURATION)
        for rainy_trip_n_duration in rainy_trips_duration_batch:
            packet.add_byte(self.VALUE)
            self.__add_date_n_duration(packet, rainy_trip_n_duration[0], rainy_trip_n_duration[1])
        packet.add_byte(self.FINISHED)

    def add_station_occurrence_batch(self, packet, station_occurrence_batch):
        packet.add_byte(self.STATION_OCCURRENCE)
        for station_occurrence in station_occurrence_batch:
            packet.add_byte(self.VALUE)
            self.__add_year_city_n_station_name_to_packet(packet, station_occurrence[0], station_occurrence[1],
                                                          station_occurrence[2])
        packet.add_byte(self.FINISHED)

    def __add_year_city_n_station_name_to_packet(self, packet, year, city_name, station_name):
        packet.add_n_byte_number(super().TWO_BYTES, year)
        packet.add_string_and_length(city_name)
        packet.add_string_and_length(station_name)

    def add_station_name_distance_n_year(self, packet, year, station_name, distance):
        packet.add_byte(self.DISTANCE_OCCURRENCE)
        packet.add_n_byte_number(super().TWO_BYTES, year)
        packet.add_string_and_length(station_name)
        packet.add_float(distance)

    def __recv_rainy_trip_duration_batch(self, byte_stream):
        rainy_trip_duration_batch = []
        byte = super()._recv_byte(byte_stream)
        while byte != self.FINISHED:
            date = super()._recv_date(byte_stream)
            duration = super()._recv_n_byte_number(byte_stream, super().FOUR_BYTES)
            rainy_trip_duration_batch.append((date, duration))
            byte = self._recv_byte(byte_stream)
        return rainy_trip_duration_batch

    def __recv_station_occurrence_batch(self, byte_stream):
        station_occurrence_batch = []
        byte = super()._recv_byte(byte_stream)
        while byte != self.FINISHED:
            year = super()._recv_n_byte_number(byte_stream, super().TWO_BYTES)
            city_name = super()._recv_string(byte_stream)
            station_name = super()._recv_string(byte_stream)
            station_occurrence_batch.append((year, city_name, station_name))
            byte = self._recv_byte(byte_stream)
        return station_occurrence_batch

    def recv_results_processor_action(self, byte_stream):
        act = super()._recv_byte(byte_stream)
        if act == super().FINISHED:
            return FinishedAction()
        elif act == self.DATE_N_DURATION:
            rainy_trip_duration_batch = self.__recv_rainy_trip_duration_batch(byte_stream)
            return RainyTripAction(rainy_trip_duration_batch)
        elif act == self.STATION_OCCURRENCE:
            station_occurrence_batch = self.__recv_station_occurrence_batch(byte_stream)
            return Trip2016_17Action(station_occurrence_batch)
        elif act == self.DISTANCE_OCCURRENCE:
            year = super()._recv_n_byte_number(byte_stream, super().TWO_BYTES)
            station_name = super()._recv_string(byte_stream)
            distance = super()._recv_float(byte_stream)
            return MontrealDistanceAction(year, station_name, distance)
        else:
            return QueryAskAction()
