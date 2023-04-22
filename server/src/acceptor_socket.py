import socket
from .socket_wrapper import Socket


class AcceptorSocket():

    def __init__(self, host, port, listen_backlog):
        _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        _socket.bind((host, port))
        _socket.listen(listen_backlog)
        self._socket = _socket

    def accept(self):
        c, _addr = self._socket.accept()
        return Socket('', 0, created_socket=c)

    def shutdown_and_close(self):
        self._socket.shutdown(socket.SHUT_RDWR)
        self._socket.close()