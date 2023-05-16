
from .filter_protocol import FilterProtocol
from .packet import Packet
from .server_protocol import ServerProtocol


class QueueCommunicationHandler:

    def __init__(self, queue):
        self._queue = queue
        self._server_protocol = ServerProtocol()
        self._filter_protocol = FilterProtocol()

    def send_finished(self):
        packet = Packet()
        self._server_protocol.add_finished_to_packet(packet)
        self._queue.send(packet)

    def send_last_finished(self):
        packet = Packet()
        self._server_protocol.add_last_finished_to_packet(packet)
        self._queue.send(packet)

    def send_station_finished(self):
        packet = Packet()
        self._server_protocol.add_station_finished_to_packet(packet)
        self._queue.send(packet)

    def send_data_to_distributer(self, data_type, data):
        packet = Packet()
        self._server_protocol.add_data_to_packet(packet, data_type, data)
        self._queue.send(packet)

    def send_weather_finished_to_distributer(self):
        packet = Packet()
        self._server_protocol.add_weather_finished_to_packet(packet)
        self._queue.send(packet)

    def send_station_finished_to_distributer(self):
        packet = Packet()
        self._server_protocol.add_station_finished_to_packet(packet)
        self._queue.send(packet)

    def send_batch_to_weather_process(self, weather_batch):
        packet = Packet()
        self._server_protocol.add_weather_batch_to_packet(packet, weather_batch, throw_unnecessary_data=True) #Todo eliminar esto
        self._queue.send(packet)

    def send_batch_to_station_processes(self, station_batch):
        if len(station_batch) == 0:
            return
        packet = Packet()
        self._server_protocol.add_stations_batch_to_packet(packet, station_batch)
        self._queue.send(packet)

    def send_trip_batch_to_processes(self, trip_batch):
        if len(trip_batch) == 0:
            return
        packet = Packet()
        self._server_protocol.add_trip_batch_to_packet(packet, trip_batch)
        self._queue.send(packet)

    def send_query_ask(self):
        packet = Packet()
        self._server_protocol.add_query_ask_to_packet(packet)
        self._queue.send(packet)

    def send_query_data(self, query_data):
        packet = Packet()
        self._server_protocol.add_query_data_to_packet(packet, query_data)
        self._queue.send(packet)

    def send_station_occurrence_batch(self, trips_in_2016_or_2017):
        if len(trips_in_2016_or_2017) == 0:
            return
        packet = Packet()
        self._filter_protocol.add_station_occurrence_batch(packet, trips_in_2016_or_2017)
        self._queue.send(packet)

    def send_rainy_trip_duration_batch(self, rainy_trips_duration_batch):
        packet = Packet()
        self._filter_protocol.add_rainy_trip_duration_batch(packet, rainy_trips_duration_batch)
        self._queue.send(packet)

    def send_station_distance_occurrence_batch(self, station_distance_occurrence_batch):
        packet = Packet()
        self._filter_protocol.add_station_distance_occurrence_batch(packet, station_distance_occurrence_batch)
        self._queue.send(packet)

    def recv_data_distributer_action(self, packet):
        return self._server_protocol.recv_data_distributer_action(packet)

    def recv_weather_batch(self, packet):
        return self._server_protocol.recv_weather_batch_or_finished(packet)

    def recv_station_batch(self, packet):
        return self._server_protocol.recv_station_batch_or_finished(packet)

    def recv_trip_batch(self, packet):
        return self._server_protocol.recv_trip_batch_or_finished(packet)

    def recv_results_processor_action(self, packet):
        return self._filter_protocol.recv_results_processor_action(packet)

    def recv_query_data(self, packet):
        return self._server_protocol.recv_query_data(packet)

    def close(self):
        self._queue.close()

    def start_consuming(self):
        self._queue.start_recv_loop()
