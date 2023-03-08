from fastapi import APIRouter, Request
from starlette import status
from starlette.responses import JSONResponse


router = APIRouter()


@router.post(
    "/ping",
    name='basic:ping',
    status_code=status.HTTP_200_OK
)
async def ping(request: Request):
    return 'pong'
