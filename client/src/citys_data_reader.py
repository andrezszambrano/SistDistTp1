

class CityDataReader:
    def __init__(self, city_name):
        self._city_name = city_name

    def run(self, queue):
        queue.put(self._city_name)