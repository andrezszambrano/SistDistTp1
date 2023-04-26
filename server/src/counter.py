import logging


class Counter:
    def __init__(self):
        self._counter = 0

    def increase(self):
        self._counter = self._counter + 1
        #logging.debug(f"{self._counter}")
        if self._counter % 1000000 == 0:
            logging.debug(f"{self._counter}")