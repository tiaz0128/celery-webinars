from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.domain.models.user import Base


class DBEngineManager:
    _instance = None

    def __new__(cls, url=None):
        if cls._instance is None and url:
            cls._instance = create_engine(url)

        return cls._instance


def make_session():
    engine = DBEngineManager("sqlite:///./.temp/test.db")
    Base.metadata.create_all(engine)

    return Session(engine)
