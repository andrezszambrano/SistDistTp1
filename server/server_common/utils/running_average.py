import logging


class RunningAverage:
    def __init__(self, total=0, count=0, avg=None):
        self._total = total
        self._count = count
        self._avg = avg

    def recalculate_avg(self, number):
        self._total = self._total + number
        self._count = self._count + 1

    def get_avg(self):
        if self._avg is not None:
            return self._avg
        if self._count == 0:
            return 0
        return self._total / self._count
