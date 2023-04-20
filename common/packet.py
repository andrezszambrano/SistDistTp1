import logging

ONE_BYTE = 1
TWO_BYTES = 2

class Packet:
    def __init__(self):
        self._bytes = b""

    def concatenate_bytes(self, bytes):
        self._bytes = self._bytes + bytes

    def add_byte(self, byte):
        self.concatenate_bytes(byte.encode('utf-8'))

    def add_n_byte_number(self, n, number):
        BEnumber = number.to_bytes(n, byteorder='big')
        self.concatenate_bytes(BEnumber)

    def add_string_and_length(self, string):
        str_bytes = string.strip('"').encode('utf-8')
        self.add_n_byte_number(ONE_BYTE, len(str_bytes))
        self.concatenate_bytes(str_bytes)

    def add_date(self, date):
        date_bytes = date.strftime("%Y-%m-%d").strip('"').encode('utf-8')
        self.add_n_byte_number(ONE_BYTE, len(date_bytes))
        self.concatenate_bytes(date_bytes)

    def send_to_socket(self, socket):
        socket.send(self._bytes, len(self._bytes))
