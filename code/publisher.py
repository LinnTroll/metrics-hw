"""Provide class for publishing to kafka."""
import json

from kafka import KafkaProducer


class Publisher:
    # pylint: disable=too-few-public-methods
    """Class for publishing to kafka."""

    def __init__(self, topic, **kwargs):
        self.topic = topic
        self.producer = KafkaProducer(
            value_serializer=lambda m: json.dumps(m).encode("ascii"),
            **kwargs,
        )

    def send_message(self, message):
        """Send message to kafka topic."""
        self.producer.send(self.topic, message)
