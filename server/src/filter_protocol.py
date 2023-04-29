import logging

from .protocol import Protocol


class FilterProtocol(Protocol):
    DATE_N_DURATION = 'P'

    def __init__(self):
        super(FilterProtocol, self).__init__()

    def add_date_n_duration(self, packet, date, duration_sec):
        packet.add_byte(self.DATE_N_DURATION)
        packet.add_date(date)
        packet.add_n_byte_number(super().FOUR_BYTES, duration_sec)

    def recv_date_n_duration_or_finished(self, bytestream):
        act = super()._recv_byte(bytestream)
        if act == super().FINISHED:
            return None
        date = super()._recv_date(bytestream)
        duration = super()._recv_n_byte_number(bytestream, super().FOUR_BYTES)
        return (date, duration)
