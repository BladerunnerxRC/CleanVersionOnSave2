# src/timer.py

import threading

class SyncTimer:
    """
    A reusable timer that calls the provided sync_func every interval_sec.
    """

    def __init__(self, sync_func, interval_sec=300):
        self._sync       = sync_func
        self._interval   = interval_sec
        self._timer      = None

    def _run(self):
        try:
            self._sync()
        finally:
            # re-schedule
            self.start()

    def start(self):
        if self._timer is None:
            self._timer = threading.Timer(self._interval, self._run)
            self._timer.daemon = True
            self._timer.start()

    def stop(self):
        if self._timer:
            self._timer.cancel()
            self._timer = None