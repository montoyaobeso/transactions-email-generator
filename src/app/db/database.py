import logging
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from src.app.aws.secrets import get_secret

logger = logging.getLogger()
logger.setLevel(logging.INFO)

if os.environ["STAGE"] != "local":
    db_credentials = get_secret("stori-database-credentials")
    logger.info("Credentials response type:", type(db_credentials))
    logger.info("Credentials keys: ", db_credentials.keys())
    os.environ["POSTGRES_USER"] = db_credentials["username"]
    os.environ["POSTGRES_PASSWORD"] = db_credentials["password"]
    os.environ["POSTRES_HOST"] = db_credentials["host"]
    os.environ["POSTRES_DB"] = db_credentials["database"]
else:
    logger.info("Executing in local enviroment.")

SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://{os.environ['POSTGRES_USER']}:{os.environ['POSTGRES_PASSWORD']}@{os.environ['POSTRES_HOST']}/{os.environ['POSTGRES_DB']}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
