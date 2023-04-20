import logging

from .socket_wrapper import Socket

DATE = "D"
FINISHED = "F"

class Sender:
    def __init__(self, server_address):
        host, _port = server_address.split(':')
        port = int(_port)
        #self._socket = Socket(host, port)

    def send_data(self, queue):
        counter = 0
        keep_receiving = True
        while keep_receiving:
            data = queue.get()
            if data[0] == FINISHED:
                counter = counter + 1
                keep_receiving = not (counter == 3)
            else:
                logging.debug(f"{data[1][0].date} and {data[1][1].date}")
