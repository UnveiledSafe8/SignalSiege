from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

import os

SQL_PASSWORD = os.getenv("SQL_PASSWORD")
SQL_USERNAME = os.getenv("SQL_USERNAME")
POSTGRES_CONTAINER = os.getenv("POSTGRES_CONTAINER")

engine = create_engine(f"postgresql+psycopg2://{SQL_USERNAME}:{SQL_PASSWORD}@{POSTGRES_CONTAINER}:5432/signal_siege_database", echo=True)

Base = declarative_base()

Session = sessionmaker(bind=engine)