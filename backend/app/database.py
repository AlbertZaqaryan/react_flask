import os
import time

from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "mysql+pymysql://carsuser:carspassword@localhost:3306/carsdb",
)

engine = create_engine(DATABASE_URL, pool_pre_ping=True, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def wait_for_db(retries: int = 30, delay: int = 2) -> None:
    """Block until the database accepts connections (MySQL can be slow to boot)."""
    for attempt in range(1, retries + 1):
        try:
            with engine.connect():
                return
        except OperationalError:
            print(f"[db] not ready (attempt {attempt}/{retries}), retrying in {delay}s...")
            time.sleep(delay)
    raise RuntimeError("Database did not become available in time")
