import logging

from .actions.finished_action import FinishedAction
from .actions.query_ask_action import QueryAskAction
from .actions.rainy_trip_action import RainyTripAction
from .protocol import Protocol


class FilterProtocol(Protocol):
    DATE_N_DURATION = 'P'

    def __init__(self):
        super(FilterProtocol, self).__init__()

    def add_date_n_duration(self, packet, date, duration_sec):
        packet.add_byte(self.DATE_N_DURATION)
        packet.add_date(date)
        packet.add_n_byte_number(super().FOUR_BYTES, duration_sec)

    def recv_results_processor_action(self, bytestream):
        act = super()._recv_byte(bytestream)
        if act == super().FINISHED:
            return FinishedAction()
        elif act == self.DATE_N_DURATION:
            date = super()._recv_date(bytestream)
            duration = super()._recv_n_byte_number(bytestream, super().FOUR_BYTES)
            return RainyTripAction(date, duration)
        else:
            return QueryAskAction()