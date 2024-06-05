from fastapi import FastAPI
from mangum import Mangum
from dotenv import load_dotenv

load_dotenv()

# from src.api.routers import root

# from src.api.routers import presiged_url
# from src.api.routers import load_transactions
# from src.api.routers import load_transactions_s3
# from src.api.routers import account
# from src.api.routers import transaction
# from src.api.routers import send_balance

# from src.app.db import models
# from src.app.db.database import engine


# models.Base.metadata.create_all(bind=engine)

# app = FastAPI(
#     title="Transactions Email Generator",
#     description="Generate a transactions summary email.",
#     version="0.0.1",
#     contact={
#         "name": "Abraham Montoya",
#         "email": "montoyaobeso@gmail.com",
#     },
# )

# app.include_router(root.router)
# app.include_router(account.router)
# app.include_router(transaction.router)
# app.include_router(presiged_url.router)
# app.include_router(load_transactions.router)
# app.include_router(load_transactions_s3.router)
# app.include_router(send_balance.router)

# handler = Mangum(app)


from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


handler = Mangum(app)
