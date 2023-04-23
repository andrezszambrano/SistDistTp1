from multiprocessing import SimpleQueue

class ProdConsQueue:
    def __init__(self):
        self._queue = SimpleQueue()

    def get(self):
        self._queue.get()

    def put(self, data):
        self._queue.put(data)
