import json
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.exc import SQLAlchemyError

from app.config.config import Settings
from app.domain.sensor_data import Base


class Database:
    def __init__(self, settings: Settings):
        self.engine = create_engine(
            f"postgresql://{settings.db_user}:{settings.db_password}@{settings.db_host}:{settings.db_port}/{settings.db_name}",
            pool_pre_ping=True,
            echo_pool=True,
            pool_size=10,
            max_overflow=20
        )
        self.Session = scoped_session(sessionmaker(bind=self.engine))

    def get_session(self):
        return self.Session()

    def close(self):
        self.Session.remove()


def setup_database(settings: Settings):
    db = Database(settings)
    Base.metadata.create_all(db.engine)
    return db.get_session()
