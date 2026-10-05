import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

load_dotenv()

# Local default: a SQLite file. In production, DATABASE_URL points to Postgres.
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./clearclause.db")

# Hosts often hand out "postgres://..." or "postgresql://..." addresses.
# This tells SQLAlchemy to use the modern psycopg driver for them.
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+psycopg://", 1)
elif DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg://", 1)

if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    # pool_pre_ping checks a connection is alive before using it, which matters
    # because serverless databases close idle connections.
    engine = create_engine(DATABASE_URL, pool_pre_ping=True, pool_recycle=300)

SessionLocal = sessionmaker(bind=engine, autoflush=False)


class Base(DeclarativeBase):
    pass


def get_db():
    """Gives each request its own database session, then closes it."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()