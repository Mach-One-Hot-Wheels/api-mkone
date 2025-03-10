from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base
from src.auth.models import User
from src.hotwheels.models import Hotwheels
from src.base import Base
from dotenv import load_dotenv
import os

load_dotenv()

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_HOSTNAME = os.getenv("POSTGRES_HOSTNAME")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")

#DATABASE_URL = "sqlite:///database.sqlite"
DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOSTNAME}:{POSTGRES_PORT}/{POSTGRES_DB}"

engine = create_engine(DATABASE_URL)


def create_database():
    Base.metadata.create_all(bind=engine)


def get_session():
    with Session(engine) as session:
        yield session


if __name__ == "__main__":
    create_database()
