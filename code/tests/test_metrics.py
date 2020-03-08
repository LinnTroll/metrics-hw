"""Tests for metrics class."""
import unittest
from unittest.mock import patch, MagicMock, ANY

from metrics import Metrics


class TestMetrics(unittest.TestCase):
    @patch("psutil.disk_usage")
    @patch("psutil.virtual_memory")
    @patch("psutil.cpu_percent")
    def test_metrics_step(self, cpu_percent_mock, virtual_memory_mock, disk_usage_mock):
        metrics = Metrics()
        callback = MagicMock()
        metrics.add_listener(callback)
        metrics._step()
        assert callback.call_args_list == [
            ((("cpu_metrics", ANY),),),
            ((("mem_metrics", ANY),),),
            ((("disk_metrics", ANY),),),
        ]

    @patch("metrics.Metrics._step", side_effect=[None, KeyboardInterrupt])
    def test_metrics_run_interrupt(self, step_mock):
        metrics = Metrics()
        metrics.run()
        assert step_mock.call_count == 2
