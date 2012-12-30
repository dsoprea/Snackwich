
class GotoPanelException(Exception):
    _key = None

    def __init__(self, key):
        self._key = key

    @property
    def key(self):
        return self._key

class BreakSuccessionException(Exception):
    pass

class QuitException(Exception):
    pass

class RedrawException(Exception):
    pass

class QuitAndExecuteException(Exception):
    def __init__(self, posthook_cb):
        Exception.__init__(self, "Snackwich loop has been explicitly broken "
                                 "with a posthook.")

        self.__posthook_cb = posthook_cb

    @property
    def posthook_cb(self):
        return self.__posthook_cb

class PostQuitAndExecuteException(QuitAndExecuteException):
    def __init__(self, posthook_cb, result):
        QuitAndExecuteException.__init__(self, posthook_cb)

        self.__result = result

    @property
    def result(self):
        return self.__result

class PostAndGotoException(Exception):
    def __init__(self, result, next_panel=None):
        self.__result     = result
        self.__next_panel = next_panel

    @property
    def result(self):
        return self.__result

    @property
    def next_panel(self):
        return self.__next_panel

