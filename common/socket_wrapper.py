import socket

from .byte_stream import ByteStream
from .packet_sender import PacketSender


class Socket(ByteStream, PacketSender):

    def __init__(self, host, port, created_socket = None):
        super(Socket, self).__init__()
        _socket = None
        if created_socket != None:
            _socket = created_socket
        else:
            _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            _socket.connect((host, port))
        self._socket = _socket

    def getpeername(self):
        return self._socket.getpeername()

    def shutdown_and_close(self):
        self._socket.shutdown(socket.SHUT_RDWR)
        self._socket.close()

    def __send(self, buffer, length):
        sent = 0
        while sent < length:
            aux = self._socket.send(buffer[sent:])
            sent = sent + aux

    def read(self, length):
        received_data = b""
        while len(received_data) < length:
            data_chunk = self._socket.recv(length - len(received_data))
            received_data = received_data + data_chunk
        return received_data

    def send(self, packet):
        bytes = packet.get_bytes()
        self.__send(bytes, len(bytes))
