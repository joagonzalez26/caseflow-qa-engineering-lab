from collections.abc import Generator

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

from caseflow.core.config import get_settings


def create_database_engine(database_url: str) -> Engine:
    return create_engine(
        database_url,
        pool_pre_ping=True,
    )


settings = get_settings()
engine = create_database_engine(settings.database_url)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False,
)


def get_db() -> Generator[Session, None, None]:
    with SessionLocal() as session:
        yield session
