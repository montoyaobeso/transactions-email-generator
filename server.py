import fastapi, uvicorn
import os

api = fastapi.FastAPI()

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
