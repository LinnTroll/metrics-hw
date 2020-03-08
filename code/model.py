"""Provide models for storing metrics in database."""
import datetime

from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()  # pylint: disable=invalid-name


class MetricEvent(Base):
    # pylint: disable=too-few-public-methods
    """Models for storing metrics. """

    __tablename__ = "metric_events"

    id = Column(Integer, primary_key=True)
    event_time = Column(DateTime)
    hostname = Column(String(length=255))
    type = Column(String(length=32))
    data = Column(Integer)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return f"<{self.__class__.__name__} type={self.type} data={self.data}>"
