import logging
import time


class PrintingCounter:
    def __init__(self, name, module=1000):
        self._counter = 0
        self._name = name
        self._module = module
        self._start_time = time.time()
        self._last_time = self._start_time

    def increase(self):
        self._counter = self._counter + 1
        if self._counter % self._module == 0:
            now = time.time()
            secs_since_last_time = round(now - self._last_time, 4)
            ratio = round(self._module/secs_since_last_time, 1)
            logging.debug(f"{self._name}: {self._counter}. Seconds between {self._module} increase: {secs_since_last_time}s "
                        + f"Total seconds: {round(now - self._start_time, 4)}s. Ratio: {ratio}inc/s")
            self._last_time = now

    def print_final(self):
        now = time.time()
        logging.debug(f"{self._name}: {self._counter}. Total seconds: {round(now - self._start_time, 4)}s")
