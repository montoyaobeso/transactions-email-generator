import json
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from src.app.aws.secrets import get_secret

if os.environ["STAGE"] != "local":
    if "APP_RUNNER_SECRETS" in os.environ:
        db_credentials = json.loads(os.environ["APP_RUNNER_SECRETS"])
    else:
        db_credentials = get_secret("stori-database-credentials")

    os.environ["POSTGRES_USER"] = db_credentials["POSTGRES_USER"]
    os.environ["POSTGRES_PASSWORD"] = db_credentials["POSTGRES_PASSWORD"]
    os.environ["POSTGRES_HOST"] = db_credentials["POSTGRES_HOST"]
    os.environ["POSTGRES_DB"] = db_credentials["POSTGRES_DB"]

SQLALCHEMY_DATABASE_URL = f"postgresql://{os.environ['POSTGRES_USER']}:{os.environ['POSTGRES_PASSWORD']}@{os.environ['POSTGRES_HOST']}/{os.environ['POSTGRES_DB']}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
