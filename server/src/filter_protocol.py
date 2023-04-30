import logging

from .actions.finished_action import FinishedAction
from .actions.query_ask_action import QueryAskAction
from .actions.rainy_trip_action import RainyTripAction
from .actions.trip_in_2016_2917_action import Trip2016_17Action
from .protocol import Protocol


class FilterProtocol(Protocol):
    DATE_N_DURATION = 'P'
    STATION_OCCURRENCE = 'S'

    def __init__(self):
        super(FilterProtocol, self).__init__()

    def add_date_n_duration(self, packet, date, duration_sec):
        packet.add_byte(self.DATE_N_DURATION)
        packet.add_date(date)
        packet.add_n_byte_number(super().FOUR_BYTES, duration_sec)

    def add_year_city_n_station_name_to_packet(self, packet, year, city_name, station_name):
        packet.add_byte(self.STATION_OCCURRENCE)
        packet.add_n_byte_number(super().TWO_BYTES, year)
        packet.add_string_and_length(city_name)
        packet.add_string_and_length(station_name)

    def recv_results_processor_action(self, bytestream):
        act = super()._recv_byte(bytestream)
        if act == super().FINISHED:
            return FinishedAction()
        elif act == self.DATE_N_DURATION:
            date = super()._recv_date(bytestream)
            duration = super()._recv_n_byte_number(bytestream, super().FOUR_BYTES)
            return RainyTripAction(date, duration)
        elif act == self.STATION_OCCURRENCE:
            year = super()._recv_n_byte_number(bytestream, super().TWO_BYTES)
            city_name = super()._recv_string(bytestream)
            station_name = super()._recv_string(bytestream)
            return Trip2016_17Action(city_name, year, station_name)
        else:
            return QueryAskAction()