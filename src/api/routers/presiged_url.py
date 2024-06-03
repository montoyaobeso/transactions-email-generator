import os
import uuid

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from src.app.aws.s3 import create_presigned_post

router = APIRouter(
    prefix="/presigned_url",
    tags=["presigned_url"],
    responses={404: {"description": "Not found"}},
)


@router.get("")
async def presigned_url():

    response = create_presigned_post(
        bucket_name=os.environ["AWS_BUCKET_NAME"],
        object_name=f"{uuid.uuid4()}.csv",
    )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=response,
    )
