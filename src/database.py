from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

from config import settings

engine = create_engine(settings.database_url(), echo=True, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:  # pragma: no cover
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
