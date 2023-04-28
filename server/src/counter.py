import logging


class Counter:
    def __init__(self, name):
        self._counter = 0
        self._name = name

    def increase(self):
        self._counter = self._counter + 1
        #logging.debug(f"{self._counter}")
        if self._counter % 100 == 0:
            logging.debug(f"{self._name}: {self._counter}")