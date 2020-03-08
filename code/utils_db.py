"""Utils for working with db."""
import logging
import os

from sqlalchemy import create_engine
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.orm import sessionmaker


def get_db_engine():
    """Returns SQLAlchemy engine instance."""
    return create_engine(os.environ["DB_URL"])


def get_db_session():
    """Returns SQLAlchemy session connected to database."""
    Session = sessionmaker(bind=get_db_engine())  # pylint: disable=invalid-name
    return Session()


def create_table(model):
    """Create table in database for given model."""
    try:
        model.metadata.create_all(get_db_engine(), checkfirst=False)
        logging.info("Table %s created", model.__table__.name)
    except ProgrammingError:
        logging.info("Table %s already exists", model.__table__.name)
