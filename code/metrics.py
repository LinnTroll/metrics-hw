"""Module provide class for getting and publishing metrics."""
import time

import psutil


class Metrics:
    """Class for getting and publishing metrics."""

    def __init__(self, listeners=None, check_timeout=1):
        self._listeners = listeners or []
        self.check_timeout = check_timeout

    def add_listener(self, callback):
        """Add listener for publishing metrics."""
        self._listeners.append(callback)

    @staticmethod
    def get_cpu_metrics():
        """Get CPU percentage metric."""
        return "cpu_metrics", psutil.cpu_percent()

    @staticmethod
    def get_mem_metrics():
        """Get memory percentage metric."""
        return "mem_metrics", psutil.virtual_memory().percent

    @staticmethod
    def get_disk_metrics():
        """Get disk usage percentage metric."""
        return "disk_metrics", psutil.disk_usage("/").percent

    def get_metrics(self):
        """Get all metrics."""
        return (
            self.get_cpu_metrics(),
            self.get_mem_metrics(),
            self.get_disk_metrics(),
        )

    def _step(self):
        if not self._listeners:
            return

        metrics = self.get_metrics()
        for metric in metrics:
            for listener in self._listeners:
                listener(metric)

    def run(self):
        """Start process for periodical metrics publishing."""
        print(f"Start publishing metrics each {self.check_timeout} seconds")
        try:
            while True:
                self._step()
                time.sleep(self.check_timeout)
        except KeyboardInterrupt:
            print("Stop publishing")
