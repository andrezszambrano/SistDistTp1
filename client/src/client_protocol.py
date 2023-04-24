
from .protocol import Protocol

class ClientProtocol(Protocol):

    def __init__(self):
        super(ClientProtocol, self).__init__()

    def add_stations_chunk_to_packet(self, packet, stations_list):
        for station in stations_list:
            super().add_station_to_packet(packet, station)

    def add_weather_chunk_to_packet(self, packet, weather_list):
        for weather in weather_list:
            super().add_weather_to_packet(packet, weather)

    def add_request_for_ack_to_packet(self, packet):
        packet.add_byte(super().ASK_ACK)

    def recv_ack(self, byte_stream):
        super()._recv_byte(byte_stream)
