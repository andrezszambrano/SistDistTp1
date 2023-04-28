import logging
from multiprocessing import SimpleQueue, Queue

from ..packet import Packet
from ..packet_sender import PacketSender


class PublSubsQueue(PacketSender):
    def __init__(self, subscribers_amount):
        self._queues = {}
        for i in range(subscribers_amount):
            self._queues.update({i: Queue()})

    def get_packet(self, queue_id):
        return Packet(self._queues[queue_id].get())

    def send(self, packet):
        for queue in self._queues.values():
            #logging.debug(f"{queue.full()}")
            queue.put(packet.get_bytes())
