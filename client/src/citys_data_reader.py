import logging
from datetime import datetime

from .chunk_file_reader import ChunkFileReader
from .sender import FINISHED, DATE
from .weather import Weather

FILEPATH = "data/"
FIVE_MB = 5 * 1024 * 1024 # 5 MB
WEATHER = "weather.csv"

def row_to_weather_obj(row):
    return Weather(datetime.strptime(row[0], '%Y-%m-%d').date(), float(row[1]), float(row[2]), float(row[3]),
                              float(row[4]), float(row[5]), float(row[6]), float(row[7]), float(row[8]), float(row[9]),
                              float(row[10]), float(row[11]), float(row[12]), float(row[13]), float(row[14]),
                              float(row[15]), float(row[16]), float(row[17]), float(row[18]), float(row[19]))


class CityDataReader:
    def __init__(self, city_name):
        self._city_name = city_name

    def run(self, queue):
        weather_chunk_generator = ChunkFileReader(f"{FILEPATH}{self._city_name}/weather.csv")
        for chunk in weather_chunk_generator.get_chunks(FIVE_MB, row_to_weather_obj):
            queue.put((DATE,chunk))
        queue.put(FINISHED)
