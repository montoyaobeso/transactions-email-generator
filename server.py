import os
import uvicorn
from fastapi import FastAPI

from dotenv import load_dotenv

load_dotenv()


from src.api.routers import account
from src.api.routers import load_transactions
from src.api.routers import load_transactions_s3
from src.api.routers import presiged_url
from src.api.routers import root
from src.api.routers import send_balance
from src.api.routers import transaction


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
        port=int(os.getenv("PORT", 8080)),
        log_level=os.getenv("LOG_LEVEL", "info"),
        proxy_headers=True,
    )
