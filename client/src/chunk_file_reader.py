import csv


class ChunkFileReader:
    def __init__(self, path, chunk_size, row_into_obj_fn):
        self._path = path
        self._chunk_size = chunk_size
        self._row_into_obj_fn = row_into_obj_fn

    def get_chunks(self):
        with open(self._path, 'r') as file:
            reader = csv.reader(file, quoting=csv.QUOTE_MINIMAL)
            next(reader)
            chunk = []
            current_size = 0
            for row in reader:
                obj = self._row_into_obj_fn(row)
                chunk.append(obj)
                current_size += len(str(row))
                if current_size > self._chunk_size:
                    yield chunk
                    chunk = []
                    current_size = 0
            if chunk:
                yield chunk

