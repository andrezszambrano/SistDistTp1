import logging
from datetime import datetime

from .chunk_file_reader import ChunkFileReader
from .sender import FINISHED, WEATHER_DATA, STATION_DATA, TRIP_DATA, WEATHER_FINISHED
from .station import Station
from .weather import Weather
from .trip import Trip

DATA_PATH = "data/"
FIVE_MB = 5 * 1024 * 1024  # 5 MB
WEATHER = "weather.csv"
STATIONS = "stations.csv"
TRIPS = "rainy_trips.csv"

def row_to_weather_obj(row, city_name):
    return Weather(city_name, datetime.strptime(row[0], '%Y-%m-%d').date(), float(row[1]), float(row[2]), float(row[3]),
                   float(row[4]), float(row[5]), float(row[6]), float(row[7]), float(row[8]), float(row[9]),
                   float(row[10]), float(row[11]), float(row[12]), float(row[13]), float(row[14]),
                   float(row[15]), float(row[16]), float(row[17]), float(row[18]), float(row[19]))


def row_to_station_obj(row, city_name):
    latitude = None if row[2] == '' else float(row[2])
    longitude = None if row[3] == '' else float(row[3])
    return Station(city_name, int(row[0]), row[1], latitude, longitude, int(row[4]))

def row_to_trip_obj(row, city_name):
    IS_MEMBER = 1
    duration = int(round(float(row[4])))
    if duration < 0:
        duration = 0
    return Trip(city_name, datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S'), int(row[1]),
                datetime.strptime(row[2], '%Y-%m-%d %H:%M:%S'), int(row[3]), duration,
                int(row[5]) == IS_MEMBER, int(row[6]))


class CityDataReader:
    def __init__(self, city_name, queue):
        self._city_name = city_name
        self._queue = queue

    def run(self):
        weather_chunk_generator = ChunkFileReader(f"{DATA_PATH}{self._city_name}/{WEATHER}", FIVE_MB,
                                                  row_to_weather_obj, self._city_name)
        self.__send_chunks(weather_chunk_generator, WEATHER_DATA, WEATHER_FINISHED)
        logging.info(f"{self._city_name}: Weather data read")
        stations_chunk_generator = ChunkFileReader(f"{DATA_PATH}{self._city_name}/{STATIONS}", FIVE_MB,
                                                   row_to_station_obj, self._city_name)
        self.__send_chunks(stations_chunk_generator, STATION_DATA, 'p')
        logging.info(f"{self._city_name}: Station data read")
        trips_chunk_generator = ChunkFileReader(f"{DATA_PATH}{self._city_name}/{TRIPS}", 5 * 1024,
                                                   row_to_trip_obj, self._city_name)
        self.__send_chunks(trips_chunk_generator, TRIP_DATA, 'o')
        logging.info(f"{self._city_name}: Trip data read")
        self._queue.put(FINISHED)

    def __send_chunks(self, chunk_generator, data_type, finished_char):
        if data_type == TRIP_DATA:
            for chunk in chunk_generator.get_chunks():
                self._queue.put((data_type, chunk))
                break
        else:
            for chunk in chunk_generator.get_chunks():
                self._queue.put((data_type, chunk))
        self._queue.put(finished_char)