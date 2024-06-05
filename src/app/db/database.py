import logging
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from src.app.aws.secrets import get_secret

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def set_credentials():
    db_credentials = get_secret("stori-database-credentials")
    logger.info(type(db_credentials))
    logger.info(db_credentials.keys())
    os.environ["POSTGRES_USER"] = db_credentials["username"]
    os.environ["POSTGRES_PASSWORD"] = db_credentials["password"]
    os.environ["POSTRES_HOST"] = db_credentials["host"]
    os.environ["POSTRES_DB"] = db_credentials["database"]


if os.environ["STAGE"] != "local":
    set_credentials()


SQLALCHEMY_DATABASE_URL = f"postgresql://{os.environ['POSTGRES_USER']}:{os.environ['POSTGRES_PASSWORD']}@{os.environ['POSTRES_HOST']}/{os.environ['POSTGRES_DB']}"
try:
    engine = create_engine(SQLALCHEMY_DATABASE_URL)

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    Base = declarative_base()

except Exception as exc:
    logger.error("ERROR: Connection to RDS for PostgreSQL instance failed", exc)
    raise exc

logger.info("SUCCESS: Connection to RDS for PostgreSQL instance succeeded")
