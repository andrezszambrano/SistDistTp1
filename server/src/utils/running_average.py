

class RunningAverage:
    def __init__(self):
        self._total = 0
        self._count = 0

    def recalculate_avg(self, number):
        self._total = self._total + number
        self._count = self._count + 1
        return self._total / self._count

    def get_avg(self):
        if self._total == 0:
            return 0
        return self._total / self._count
