import threading, integration

class SyncTimer:
    def __init__(self, interval_sec=300):
        self.interval = interval_sec
        self.running = False
        self.thread = None

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self.loop)
        self.thread.start()

    def loop(self):
        while self.running:
            integration.sync_latest_rename()
            threading.Event().wait(self.interval)

    def stop(self):
        self.running = False
