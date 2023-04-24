import datetime
import struct

MONTREAL = "montreal"
WASHINGTON = "washington"
TORONTO = "toronto"

class Protocol:
    NO_FLOAT = 'N'
    FLOAT = 'F'
    WEATHER_DATA = 'W'
    STATION_DATA = 'S'
    FINISHED = 'F'
    ASK_ACK = 'A'
    ACK = 'O'
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
        return datetime.date.fromisoformat(date_str)

    def _recv_float_else_none(self, byte_stream):
        aux = self._recv_byte(byte_stream)
        if aux == self.NO_FLOAT:
            return None
        else:
            float_bytes = byte_stream.read(self.FOUR_BYTES)
            return struct.unpack('f', float_bytes)[0]

    def _add_float_else_none(self, packet, float_number):
        if float_number is None:
            packet.add_byte(self.NO_FLOAT)
        else:
            packet.add_byte(self.FLOAT)
            packet.add_float(float_number)

    def add_finished_to_packet(self, packet):
        packet.add_byte(self.FINISHED)
