import logging


class Station:
    def __init__(self, code, name, latitude, longitude, yearid):
        self.code = code
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.yearid = yearid

    def info(self):
        return f"STATION: {self.code}, {self.name}, {self.latitude}, {self.longitude}, {self.yearid}"
