"""Integration tests for checking work with kafka and database."""
import time
import unittest
from unittest.mock import patch, MagicMock
from uuid import uuid4

import timeout_decorator

from dbwriter import main as dbwriter_main
from model import MetricEvent
from utils_db import get_db_session
from utils_kafka import get_publisher, get_subscriber


class StopTestSuccessException(Exception):
    pass


class TestIntegration(unittest.TestCase):
    @timeout_decorator.timeout(60, timeout_exception=TimeoutError)
    @patch("kafka.consumer.group.KafkaConsumer.commit")
    def test_kafka_integration(self, consumer_commit_mock):
        publisher = get_publisher()
        test_hostname = f"test_host_{uuid4().hex}"
        publisher.send_message({
            "hostname": test_hostname,
            "event_time": time.time(),
            "type": "test",
            "data": 0,
        })

        def callback(messages):
            for message in messages:
                hostname = message.get("hostname")
                if hostname == test_hostname:
                    raise StopTestSuccessException

        subscriber = get_subscriber()
        subscriber.add_listener(callback)
        try:
            subscriber.run()
        except StopTestSuccessException:
            pass

    @patch("kafka.consumer.group.KafkaConsumer.commit")
    @patch("kafka.consumer.group.KafkaConsumer.poll")
    @patch("kafka.consumer.group.KafkaConsumer.__init__", return_value=None)
    def test_database_integration(self, consumer_mock, consumer_poll_mock, consumer_commit_mock):
        test_event_time = time.time()
        test_hostname = f"test_host_{uuid4().hex}"
        consumer_poll_mock.side_effect = [
            {},
            {"": [
                MagicMock(value={"event_time": test_event_time, "hostname": test_hostname, "type": "t1", "data": 1}),
            ]},
            KeyboardInterrupt,
        ]
        dbwriter_main()
        session = get_db_session()
        db_item = session.query(MetricEvent).filter(MetricEvent.hostname == test_hostname).first()
        assert db_item
