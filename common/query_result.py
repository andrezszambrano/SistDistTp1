import logging


class QueryResult:
    def __init__(self, date_to_duration_avg, final_result):
        self.date_to_duration_avg = date_to_duration_avg
        self.final_result = final_result

    def set_final_result(self):
        self.final_result = True

    def print(self):
        to_print_vec = [""]
        if self.final_result:
            to_print_vec.append("FINAL RESULT")
        else:
            to_print_vec.append("PARTIAL RESULT")
        if not bool(self.date_to_duration_avg):
            to_print_vec.append("No date average yet")
        else:
            for date in self.date_to_duration_avg:
                if self.date_to_duration_avg[date].get_avg() > 0:
                    to_print_vec.append(f"\t{date}: {self.date_to_duration_avg[date].get_avg()}")
        to_print = "\n".join(to_print_vec)
        logging.info(f"{to_print}")
