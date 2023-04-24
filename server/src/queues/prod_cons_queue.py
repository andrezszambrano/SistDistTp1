import logging
from multiprocessing import SimpleQueue

from ..packet import Packet
from ..packet_sender import PacketSender


class ProdConsQueue(PacketSender):
    def __init__(self):
        super(ProdConsQueue, self).__init__()
        self._queue = SimpleQueue()

    def get_packet(self, _queue_id):
        return Packet(self._queue.get())

    def send(self, packet):
        self._queue.put(packet.get_bytes())
