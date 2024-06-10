import os
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI

load_dotenv()


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


if __name__ == "__main__":
    print("Starting webserver...")
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=int(os.getenv("SERVER_PORT", 8080)),
        log_level=os.getenv("LOG_LEVEL", "info"),
        proxy_headers=True,
    )
