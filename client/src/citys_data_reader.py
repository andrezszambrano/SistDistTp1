import csv
import logging
from datetime import datetime

from .weather import Weather

FILEPATH = "data/"


class CityDataReader:
    def __init__(self, city_name):
        self._city_name = city_name

    def run(self, queue):
        weather = list(self.get_weather())
        queue.put(weather)

    def get_weather(self):
        with open(f"{FILEPATH}{self._city_name}/weather.csv", 'r') as file:
            reader = csv.reader(file, quoting=csv.QUOTE_MINIMAL)
            next(reader)
            for row in reader:
                yield Weather(datetime.strptime(row[0], '%Y-%m-%d').date(), float(row[1]), float(row[2]), float(row[3]),
                              float(row[4]), float(row[5]), float(row[6]), float(row[7]), float(row[8]), float(row[9]),
                              float(row[10]), float(row[11]), float(row[12]), float(row[13]), float(row[14]),
                              float(row[15]), float(row[16]), float(row[17]), float(row[18]), float(row[19]))