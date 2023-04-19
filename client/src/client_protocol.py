from .protocol import Protocol
from .packet import Packet

class ClientProtocol(Protocol):

    def __init__(self):
        super(ClientProtocol, self).__init__()

    def send(self):
        pass
