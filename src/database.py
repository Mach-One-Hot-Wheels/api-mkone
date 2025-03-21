from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from src.auth.models import User
from src.hotwheels.models import Hotwheels
from src.collections.models import Collection, CollectionItem
from src.wishlist.models import Wishlist
from src.user_hotwheels.models import UserHotwheels #, UserHotwheelsSale
from src.base import Base
from dotenv import load_dotenv
import pandas as pd
import os

load_dotenv()

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_HOSTNAME = os.getenv("POSTGRES_HOSTNAME")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")


DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOSTNAME}:{POSTGRES_PORT}/{POSTGRES_DB}"

engine = create_engine(DATABASE_URL)


def create_database():
    Base.metadata.create_all(bind=engine)


def get_session():
    with Session(engine) as session:
        yield session


def add_hotwheels():
    df = pd.read_csv("other/hotwheels.csv")
    df.to_sql("hotwheels", engine, if_exists="append", index=False)


if __name__ == "__main__":
    create_database()
    add_hotwheels()
    print("Database created successfully")
