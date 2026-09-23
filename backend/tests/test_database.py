from caseflow.db.session import create_database_engine


def test_database_engine_uses_postgresql_psycopg() -> None:
    engine = create_database_engine(
        "postgresql+psycopg://user:password@localhost:5432/test_database"
    )

    assert engine.dialect.name == "postgresql"
    assert engine.url.drivername == "postgresql+psycopg"
