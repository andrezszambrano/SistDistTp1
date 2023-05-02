

class QueryData:
    def __init__(self, date_to_duration_avg, year_to_station_to_counter, station_to_distance_avg, final_data):
        self.date_to_duration_avg = date_to_duration_avg
        self.year_to_station_to_counter = year_to_station_to_counter
        self.station_to_distance_avg = station_to_distance_avg
        self.final_data = final_data

    def set_final_data(self):
        self.final_data = True
