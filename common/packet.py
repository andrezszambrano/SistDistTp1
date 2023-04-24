import struct

from .byte_stream import ByteStream

ONE_BYTE = 1
TWO_BYTES = 2
TRUE_NUM = 1
FALSE_NUM = 0


class Packet(ByteStream):

    def __init__(self, bytes=b""):
        super(Packet).__init__()
        self._bytes = bytes
        self._read_counter = 0

    def __concatenate_bytes(self, bytes):
        self._bytes = self._bytes + bytes

    def get_bytes(self):
        return self._bytes

    def add_byte(self, byte):
        self.__concatenate_bytes(byte.encode('utf-8'))

    def add_n_byte_number(self, n, number):
        BEnumber = number.to_bytes(n, byteorder='big')
        self.__concatenate_bytes(BEnumber)

    def add_float(self, float):
        float_bytes = struct.pack('f', float)
        self.__concatenate_bytes(float_bytes)

    def add_boolean(self, boolean):
        if boolean:
            self.add_n_byte_number(ONE_BYTE, TRUE_NUM)
        else:
            self.add_n_byte_number(ONE_BYTE, FALSE_NUM)

    def add_string_and_length(self, string):
        str_bytes = string.strip('"').encode('utf-8')
        self.add_n_byte_number(ONE_BYTE, len(str_bytes))
        self.__concatenate_bytes(str_bytes)

    def add_date(self, date):
        date_bytes = date.strftime("%Y-%m-%d").strip('"').encode('utf-8')
        self.add_n_byte_number(ONE_BYTE, len(date_bytes))
        self.__concatenate_bytes(date_bytes)

    def add_data_and_time(self, date_time):
        date_time_bytes = date_time.strftime('%Y-%m-%d %H:%M:%S').encode('utf-8')
        self.add_n_byte_number(ONE_BYTE, len(date_time_bytes))
        self.__concatenate_bytes(date_time_bytes)

    def read(self, length):
        bytes = self._bytes[self._read_counter: self._read_counter + length]
        self._read_counter = self._read_counter + length
        return bytes
