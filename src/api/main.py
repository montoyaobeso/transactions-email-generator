from fastapi import FastAPI
from mangum import Mangum

from src.api.routers import root

from src.api.routers import send_summary

from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="Transactions Email Generator",
    description="Generate a transactions summary email.",
    version="0.0.1",
    contact={
        "name": "Abraham Montoya",
        "email": "montoyaobeso@gmail.com",
    },
)

app.include_router(root.router)
app.include_router(send_summary.router)

handler = Mangum(app)
