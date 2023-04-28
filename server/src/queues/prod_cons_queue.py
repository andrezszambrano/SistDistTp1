import logging
from multiprocessing import SimpleQueue, Queue

from ..packet import Packet
from ..packet_sender import PacketSender


class ProdConsQueue(PacketSender):
    def __init__(self):
        super(ProdConsQueue, self).__init__()
        self._queue = Queue()

    def get_packet(self, _queue_id):
        return Packet(self._queue.get())

    def send(self, packet):
        #logging.debug(f"{self._queue.full()}")
        self._queue.put(packet.get_bytes())
