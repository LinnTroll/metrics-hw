"""Utils for working with db."""
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def get_db_session():
    """Returns SQLAlchemy session connected to database."""
    db_engine = create_engine(os.environ["DB_URL"])
    Session = sessionmaker(bind=db_engine)  # pylint: disable=invalid-name
    return Session()
