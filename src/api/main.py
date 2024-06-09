from fastapi import FastAPI
from mangum import Mangum

from dotenv import load_dotenv

load_dotenv()


import logging

logger = logging.getLogger()
from src.api.routers import account

logger.info("account route imported")

from src.api.routers import load_transactions

logger.info("load_transactions route imported")

from src.api.routers import load_transactions_s3

logger.info("load_transactions_s3 route imported")

from src.api.routers import presiged_url

logger.info("presiged_url route imported")

from src.api.routers import root

logger.info("root route imported")

from src.api.routers import send_balance

logger.info("send_balance route imported")

from src.api.routers import transaction

logger.info("transaction route imported")


app = FastAPI(
    title="Transactions Email Generator",
    description="Manage accounts, transactions and send balances to registered email.",
    version="0.0.1",
    contact={
        "name": "Abraham Montoya",
        "email": "montoyaobeso@gmail.com",
    },
)

app.include_router(root.router)
app.include_router(account.router)
app.include_router(transaction.router)
app.include_router(presiged_url.router)
app.include_router(load_transactions.router)
app.include_router(load_transactions_s3.router)
app.include_router(send_balance.router)


handler = Mangum(app)
