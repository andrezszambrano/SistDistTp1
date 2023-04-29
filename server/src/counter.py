import logging


class Counter:
    def __init__(self, name, module=1000):
        self._counter = 0
        self._name = name
        self._module = module

    def increase(self):
        self._counter = self._counter + 1
        if self._counter % self._module == 0:
            logging.debug(f"{self._name}: {self._counter}")