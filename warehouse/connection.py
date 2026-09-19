from pathlib import Path
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine


PROJECT_ROOT = Path(__file__).resolve().parents[1]

load_dotenv(PROJECT_ROOT / ".env")


def get_database_url() -> str:
    """Build the PostgreSQL connection URL from environment variables."""
    host = os.getenv("POSTGRES_HOST", "localhost")
    port = os.getenv("POSTGRES_PORT", "5432")
    database = os.getenv("POSTGRES_DB", "pro_data")
    user = os.getenv("POSTGRES_USER", "pro_data")
    password = os.getenv("POSTGRES_PASSWORD", "")

    return (
        f"postgresql+psycopg://{user}:{password}"
        f"@{host}:{port}/{database}"
    )


def create_engine_instance() -> Engine:
    """Create a SQLAlchemy engine for the warehouse."""
    return create_engine(
        get_database_url(),
        pool_pre_ping=True,
        future=True,
    )


def check_connection() -> bool:
    """Return True when the warehouse accepts a database query."""
    engine = create_engine_instance()

    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return True
    finally:
        engine.dispose()


if __name__ == "__main__":
    if check_connection():
        print("Database connection: OK")
    else:
        print("Database connection: FAILED")
