"""Tests for database writer consumer."""
import datetime
import time
import unittest
from unittest.mock import patch, MagicMock

from dbwriter import main
from model import MetricEvent


class TestDBWriter(unittest.TestCase):
    @patch("sqlalchemy.orm.session.Session.bulk_save_objects")
    @patch("kafka.consumer.group.KafkaConsumer.commit")
    @patch("kafka.consumer.group.KafkaConsumer.poll")
    @patch("kafka.consumer.group.KafkaConsumer.__init__", return_value=None)
    @patch("sqlalchemy.engine.create_engine")
    def test_write_to_db(self, create_engine_mock, consumer_mock, consumer_poll_mock,
                         consumer_commit_mock, bulk_save_objects_mock):
        time1 = time.time() - 500
        time2 = time.time()
        consumer_poll_mock.side_effect = [
            {},
            {"": [
                MagicMock(value={"event_time": time1, "hostname": "h1", "type": "t1", "data": 1}),
                MagicMock(value={"event_time": time2, "hostname": "h2", "type": "t2", "data": 2}),
            ]},
            KeyboardInterrupt,
        ]
        main()
        events = bulk_save_objects_mock.call_args[0][0]
        assert len(events) == 2
        event1, event2 = events
        assert isinstance(event1, MetricEvent)

        assert event1.hostname == "h1"
        assert event1.type == "t1"
        assert event1.event_time == datetime.datetime.fromtimestamp(time1)
        assert event1.data == 1

        assert event2.hostname == "h2"
        assert event2.type == "t2"
        assert event2.event_time == datetime.datetime.fromtimestamp(time2)
        assert event2.data == 2

    @patch("subscriber.Subscriber._step", side_effect=[None, KeyboardInterrupt])
    @patch("kafka.consumer.group.KafkaConsumer.__init__", return_value=None)
    @patch("sqlalchemy.engine.create_engine")
    def test_run_interrupt(self, create_engine_mock, consumer_mock, step_mock):
        main()
        assert step_mock.call_count == 2
