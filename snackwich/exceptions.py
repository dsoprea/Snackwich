
class GotoPanelException(Exception):
    _key = None

    def __init__(self, key):
        self._key = key

    @property
    def key(self):
        return self._key

class BreakSuccessionException(Exception):
    pass
