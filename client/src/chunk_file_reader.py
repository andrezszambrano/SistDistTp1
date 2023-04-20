import csv


class ChunkFileReader:
    def __init__(self, path):
        self._path = path

    def get_chunks(self, chunk_size, row_into_obj_fn):
        with open(self._path, 'r') as file:
            reader = csv.reader(file, quoting=csv.QUOTE_MINIMAL)
            next(reader)
            chunk = []
            current_size = 0
            for row in reader:
                obj = row_into_obj_fn(row)
                chunk.append(obj)
                current_size += len(str(row))
                if current_size > chunk_size:
                    yield chunk
                    chunk = []
                    current_size = 0
            if chunk:
                yield chunk

