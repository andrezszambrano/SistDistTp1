from .mutable_boolean import MutableBoolean


class DataDistributer:
    def __init__(self, queue):
        self._queue = queue

    def run(self):
        finished_bool = MutableBoolean(False)
        while True:
            action = self.__get_action_from_queue()
            action.perform_action(finished_bool)


    def __get_action_from_queue(self):
        bytes = self._queue.get()
        type = bytes.read(1)

        while byte != b"":
            # Do something with the byte
            print(byte)
            byte = f.read(1)

    def __read_n_bytes(self, bytes, n):
        return bytes.read(n)
