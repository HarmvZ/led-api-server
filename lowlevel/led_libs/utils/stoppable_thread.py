import threading

class StoppableThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition.
    https://stackoverflow.com/a/325528
    """

    def __init__(self, strip, kwargs={}):
        super(StoppableThread, self).__init__()
        self._stop_event = threading.Event()
        self.strip = strip
        self.kwargs = kwargs

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()