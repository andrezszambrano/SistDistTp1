
from .protocol import Protocol

class ClientProtocol(Protocol):

    def __init__(self):
        super(ClientProtocol, self).__init__()

    def add_stations_chunk_to_packet(self, packet, city_name, stations_list):
        for station in stations_list:
            super()._add_station_to_packet(packet, city_name, station)

    def add_weather_chunk_to_packet(self, packet, city_name, weather_list):
        for weather in weather_list:
            super()._add_weather_to_packet(packet, city_name, weather)

    def add_request_for_ack_to_packet(self, packet):
        packet.add_byte(super().ASK_ACK)
