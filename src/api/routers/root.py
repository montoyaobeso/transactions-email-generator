from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

router = APIRouter(
    prefix="",
    tags=["root"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def root():
    """Get a welcome messge from the API."""
    return JSONResponse(
        content={"message": "Welcome to transactions email generator API."},
        status_code=status.HTTP_200_OK,
    )
