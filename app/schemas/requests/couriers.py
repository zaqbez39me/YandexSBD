from pydantic import BaseModel

from app.schemas.models.couriers import CreateCourierDto


class CreateCourierRequest(BaseModel):
    couriers: list[CreateCourierDto]
