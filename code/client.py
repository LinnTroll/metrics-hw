"""Client for for getting and publish metrics."""

import logging
import platform
import time

from metrics import Metrics
from utils_kafka import get_publisher


def main():
    """Run metrics client."""
    logging.getLogger().setLevel(logging.INFO)
    hostname = platform.node()
    publisher = get_publisher()

    def publish_metrics(metric):
        metric_type, metric_data = metric
        message = {
            "hostname": hostname,
            "event_time": time.time(),
            "type": metric_type,
            "data": metric_data,
        }
        publisher.send_message(message)
        logging.info("Publish message: %s", message)

    metric_publisher = Metrics()
    metric_publisher.add_listener(publish_metrics)
    metric_publisher.run()


if __name__ == "__main__":
    main()
