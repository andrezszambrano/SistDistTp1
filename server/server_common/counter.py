


class Counter:
    def __init__(self, counter_goal=None):
        self._counter = 0
        self._counter_goal = counter_goal

    def increase(self):
        self._counter = self._counter + 1
        if self._counter == self._counter_goal:
            return True
        else:
            return False

    def get(self):
        return self._counter
