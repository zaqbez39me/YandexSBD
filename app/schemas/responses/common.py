from pydantic import BaseModel


class NotFoundResponse(BaseModel):
    pass


class BadRequestResponse(BaseModel):
    pass
