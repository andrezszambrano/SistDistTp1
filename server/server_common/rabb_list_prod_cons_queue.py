import logging

from .packet_sender import PacketSender
from .rabb_prod_cons_queue import RabbProdConsQueue


class RabbListProdConsQueue(PacketSender):
    def __init__(self, rabbit_channel_wrapper, queue_names):
        super(RabbListProdConsQueue, self).__init__()
        self._rabbit_prod_cons_queues = []
        for queue_name in queue_names:
            self._rabbit_prod_cons_queues.append(RabbProdConsQueue(rabbit_channel_wrapper, queue_name))

    def send(self, packet):
        for rabb_queue in self._rabbit_prod_cons_queues:
            rabb_queue.send(packet)

    def close(self):
        for rabb_queue in self._rabbit_prod_cons_queues:
            rabb_queue.close()
