import os

from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@localhost/{DB_NAME}",
                       echo=True)

Base = declarative_base()

SessionLocal = sessionmaker(bind=engine)
