

class QueryData:
    def __init__(self, date_to_duration_avg, year_to_station_to_counter, final_data):
        self.date_to_duration_avg = date_to_duration_avg
        self.year_to_station_to_counter = year_to_station_to_counter
        self.final_data = final_data

    def set_final_data(self):
        self.final_data = True
