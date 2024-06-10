import fastapi, uvicorn
from fastapi.responses import JSONResponse
import os

api = fastapi.FastAPI()


@api.get("/")
async def root():
    """Get a welcome messge from the API."""
    return JSONResponse(
        content={"message": "Welcome to transactions email generator API."},
        status_code=200,
    )


...

if __name__ == "__main__":
    print("Starting webserver...")
    uvicorn.run(
        api,
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8080)),
        log_level=os.getenv("LOG_LEVEL", "info"),
        proxy_headers=True,
    )
