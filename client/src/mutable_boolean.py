

class MutableBoolean:
    def __init__(self, boolean):
        self._boolean = boolean

    def get_boolean(self):
        return self._boolean

    def set(self, boolean):
        self._boolean = boolean
