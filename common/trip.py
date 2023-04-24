

class Trip:
    def __init__(self, city_name, start_date_time, start_station_code, end_date_time, end_station_code, duration_sec, is_member,
                 yearid):
        self.city_name = city_name
        self.start_date_time = start_date_time
        self.start_station_code = start_station_code
        self.end_date_time = end_date_time
        self.end_station_code = end_station_code
        self.duration_sec = duration_sec
        self.is_member = is_member
        self.yearid = yearid

    def info(self):
        return f"{self.city_name}: {self.start_date_time}, {self.start_station_code}, {self.end_date_time}, " \
               f"{self.end_station_code}, {self.duration_sec}, {self.is_member}, {self.yearid}"
