import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from src.app.aws.secrets import get_secret


def set_credentials():
    db_credentials = get_secret("stori-database-credentials")
    print(type(db_credentials))
    print(db_credentials.keys())
    os.environ["POSTGRES_USER"] = db_credentials["username"]
    os.environ["POSTGRES_PASSWORD"] = db_credentials["password"]
    os.environ["POSTRES_HOST"] = db_credentials["host"]
    os.environ["POSTRES_DB"] = db_credentials["database"]


if os.environ["STAGE"] != "local":
    set_credentials()

SQLALCHEMY_DATABASE_URL = f"postgresql://{os.environ['POSTGRES_USER']}:{os.environ['POSTGRES_PASSWORD']}@{os.environ['POSTRES_HOST']}/{os.environ['POSTGRES_DB']}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
