"""Tests for metrics client."""
import unittest
from unittest.mock import patch, ANY

from client import main


class TestClient(unittest.TestCase):
    @patch("platform.node", return_value="h")
    @patch("metrics.Metrics.get_metrics")
    @patch("kafka.producer.kafka.KafkaProducer.send")
    @patch("kafka.producer.kafka.KafkaProducer.__init__", return_value=None)
    def test_publish_to_kafka(self, producer_mock, send_mock, get_metrics_mock, node_mock):
        get_metrics_mock.side_effect = [
            [("t1", 0), ("t2", 1)],
            KeyboardInterrupt,
        ]
        main()
        assert send_mock.call_args_list == [
            (("metrics", {"hostname": "h", "event_time": ANY, "type": "t1", "data": 0},),),
            (("metrics", {"hostname": "h", "event_time": ANY, "type": "t2", "data": 1},),),
        ]
