"""Provide class for consuming messages from kafka."""

import json
import logging
import time

from kafka import KafkaConsumer


class Subscriber:
    """Class for consuming messages from kafka."""
    POLL_TIMEOUT = 100

    def __init__(self, topic, listeners=None, max_records=1000, **kwargs):
        self._listeners = listeners or []
        self.consumer = KafkaConsumer(
            topic,
            enable_auto_commit=False,
            value_deserializer=json.loads,
            max_poll_records=max_records,
            **kwargs,
        )

    def add_listener(self, callback):
        """Add listener for event subscription."""
        self._listeners.append(callback)

    def _step(self):
        if not self._listeners:
            return 1

        events = []
        messages = self.consumer.poll(timeout_ms=self.POLL_TIMEOUT)
        for records in messages.values():
            for record in records:
                events.append(record.value)
        if events:
            if all([listener(events) for listener in self._listeners]):
                self.consumer.commit()
                logging.info("Consumed %s events", len(events))
            else:
                logging.error("Can't consume events")
        else:
            return 1

        return None

    def run(self):
        """Start consuming messages."""
        print(f"Start metrics consumer")
        try:
            while True:
                timeout = self._step()
                if timeout:
                    time.sleep(timeout)
        except KeyboardInterrupt:
            print("Stop metrics consumer")
