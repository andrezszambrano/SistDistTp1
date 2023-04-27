import logging


class RunningAverage:
    def __init__(self, total=0, count=0):
        self._total = total
        self._count = count

    @classmethod
    def join_running_averages(cls, r_avg1, r_avg2):
        return cls(r_avg1._total + r_avg2._total, r_avg1._count + r_avg2._count)

    def recalculate_avg(self, number):
        self._total = self._total + number
        self._count = self._count + 1

    def get_avg(self):
        if self._total == 0:
            return 0
        return self._total / self._count
