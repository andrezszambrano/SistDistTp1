from datetime import datetime

from .chunk_file_reader import ChunkFileReader
from .sender import FINISHED, WEATHER_DATA, STATION_DATA
from .station import Station
from .weather import Weather

DATA_PATH = "data/"
FIVE_MB = 5 * 1024 * 1024  # 5 MB
WEATHER = "weather.csv"
STATIONS = "stations.csv"


def row_to_weather_obj(row):
    return Weather(datetime.strptime(row[0], '%Y-%m-%d').date(), float(row[1]), float(row[2]), float(row[3]),
                   float(row[4]), float(row[5]), float(row[6]), float(row[7]), float(row[8]), float(row[9]),
                   float(row[10]), float(row[11]), float(row[12]), float(row[13]), float(row[14]),
                   float(row[15]), float(row[16]), float(row[17]), float(row[18]), float(row[19]))


def row_to_station_obj(row):
    latitude = None if row[2] == '' else float(row[2])
    longitude = None if row[3] == '' else float(row[3])
    return Station(int(row[0]), row[1], latitude, longitude, int(row[4]))


class CityDataReader:
    def __init__(self, city_name, queue):
        self._city_name = city_name
        self._queue = queue

    def run(self):
        weather_chunk_generator = ChunkFileReader(f"{DATA_PATH}{self._city_name}/{WEATHER}", FIVE_MB,
                                                  row_to_weather_obj)
        self.__send_chunks(weather_chunk_generator, WEATHER_DATA)
        stations_chunk_generator = ChunkFileReader(f"{DATA_PATH}{self._city_name}/{STATIONS}", FIVE_MB,
                                                   row_to_station_obj)
        self.__send_chunks(stations_chunk_generator, STATION_DATA)
        self._queue.put(FINISHED)

    def __send_chunks(self, chunk_generator, data_type):
        for chunk in chunk_generator.get_chunks():
            self._queue.put((data_type, self._city_name, chunk))
