import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from src.app.aws.secrets import get_secret

if os.environ["STAGE"] != "local" and "POSTGRES_HOST" not in os.environ:
    db_credentials = get_secret("stori-database-credentials")
    os.environ["POSTGRES_USER"] = db_credentials["username"]
    os.environ["POSTGRES_PASSWORD"] = db_credentials["password"]
    os.environ["POSTGRES_HOST"] = db_credentials["host"]
    os.environ["POSTGRES_DB"] = db_credentials["database"]

SQLALCHEMY_DATABASE_URL = f"postgresql://{os.environ['POSTGRES_USER']}:{os.environ['POSTGRES_PASSWORD']}@{os.environ['POSTGRES_HOST']}/{os.environ['POSTGRES_DB']}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
