import re
from sqlalchemy import create_engine

# Try to import declarative_base from the new location in SQLAlchemy 2.x
try:
    from sqlalchemy.orm import declarative_base
except ImportError:
    # Fall back to the old location for SQLAlchemy 1.x
    from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import sessionmaker
import os

SQLALCHEMY_DATABASE_URL = os.getenv(
    "SQLALCHEMY_DATABASE_URL", "sqlite:////opt/chatsql/db/chatsql.db"
)

if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    db_file = re.sub("sqlite.*:///", "", SQLALCHEMY_DATABASE_URL)
    os.makedirs(os.path.dirname(db_file), exist_ok=True)
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False},  # is needed only for SQLite
    )
else:
    engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
