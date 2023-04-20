import logging

from .socket_wrapper import Socket


class Sender:
    def __init__(self, server_address):
        host, _port = server_address.split(':')
        port = int(_port)
        #self._socket = Socket(host, port)

    def send_data(self, queue):
        for _i in list(range(3)):
            data = queue.get()
            logging.debug(f"{data}")
