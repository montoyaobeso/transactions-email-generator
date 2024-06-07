from dotenv import load_dotenv
from fastapi import FastAPI
from mangum import Mangum

load_dotenv()

# from src.app.db import models
# from src.app.db.database import engine
# models.Base.metadata.create_all(bind=engine)

from src.api.routers import (
    account,
    load_transactions,
    load_transactions_s3,
    presiged_url,
    root,
    send_balance,
    transaction,
)

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
