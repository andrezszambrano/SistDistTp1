


class Counter:
    def __init__(self):
        self._counter = 0

    def increase(self):
        self._counter = self._counter + 1

    def get(self):
        return self._counter
