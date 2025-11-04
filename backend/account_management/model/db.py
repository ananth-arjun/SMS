from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from os import getenv

DATABASE_URL = getenv("DATABASE_URL",None)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

class Base(DeclarativeBase):
    pass

# Dependency for FastAPI routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Use your actual DSN; in docker compose it's usually host "postgres"
DATABASE_URL = "postgresql+psycopg2://admin:password@postgres:5432/sms"

engine = create_engine(DATABASE_URL, echo=False, future=True)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()