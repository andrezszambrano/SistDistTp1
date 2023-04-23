import struct

ONE_BYTE = 1
TWO_BYTES = 2

class Packet:
    MAX_CHUNK_SIZE = 8 * 1024  # 8KB

    def __init__(self):
        self._bytes = b""

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

    def add_string_and_length(self, string):
        str_bytes = string.strip('"').encode('utf-8')
        self.add_n_byte_number(ONE_BYTE, len(str_bytes))
        self.__concatenate_bytes(str_bytes)

    def add_date(self, date):
        date_bytes = date.strftime("%Y-%m-%d").strip('"').encode('utf-8')
        self.add_n_byte_number(ONE_BYTE, len(date_bytes))
        self.__concatenate_bytes(date_bytes)

    def send_to_socket(self, socket):
        offset = 0
        while offset < len(self._bytes):
            chunk = self._bytes[offset:offset + self.MAX_CHUNK_SIZE]
            socket.send(chunk, len(chunk))
            offset += len(chunk)
