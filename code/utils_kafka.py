"""Utils for working with kafka."""
import os

from publisher import Publisher
from subscriber import Subscriber


def get_kafka_connection_params():
    """Returns kafka connection parameters from env."""
    return {
        "bootstrap_servers": os.environ["BOOTSTRAP_SERVERS"],
        "security_protocol": os.environ["SECURITY_PROTOCOL"],
        "sasl_mechanism": os.environ["SASL_MECHANISM"],
        "sasl_plain_username": os.environ["SASL_PLAIN_USERNAME"],
        "sasl_plain_password": os.environ["SASL_PLAIN_PASSWORD"],
        "ssl_cafile": os.environ["SSL_CAFILE"],
    }


def get_publisher():
    """Returns Publisher instance connected to kafka producer."""
    return Publisher(
        topic=os.environ["TOPIC"],
        **get_kafka_connection_params(),
    )


def get_subscriber():
    """Returns Subscriber instance connected to kafka consumer."""
    return Subscriber(
        topic=os.environ["TOPIC"],
        client_id=os.environ["CLIENT_ID"],
        group_id=os.environ["GROUP_ID"],
        auto_offset_reset="earliest",
        **get_kafka_connection_params(),
    )
