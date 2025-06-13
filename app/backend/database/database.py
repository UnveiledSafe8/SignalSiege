from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine("postgresql+psycopg2://postgres:password@postgres:5432/signalsiege-database", echo=True)

Base = declarative_base()

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)