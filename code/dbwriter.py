"""Worker for receiving data from queue and sva it to database."""
import datetime
import logging

from model import MetricEvent
from utils_db import get_db_session
from utils_kafka import get_subscriber


def main():
    """Run worker."""
    logging.getLogger().setLevel(logging.INFO)
    session = get_db_session()
    subscriber = get_subscriber()

    def receive_metrics(metrics):
        events = []
        for metric in metrics:
            events.append(MetricEvent(
                event_time=datetime.datetime.fromtimestamp(metric["event_time"]),
                hostname=metric["hostname"],
                type=metric["type"],
                data=metric["data"],
            ))
        if events:
            session.bulk_save_objects(events)
            session.commit()
        return True

    subscriber.add_listener(receive_metrics)
    subscriber.run()

    session.close()


if __name__ == "__main__":
    main()
