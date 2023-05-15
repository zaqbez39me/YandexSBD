from typing import Optional

from pydantic import BaseModel

from app.schemas.models.common import int32
from app.schemas.models.couriers import CourierDto


class CreateCouriersResponse(BaseModel):
    couriers: list[CourierDto]


class GetCouriersResponse(BaseModel):
    couriers: list[CourierDto]
    limit: int32
    offset: int32


class GetCourierMetaInfoResponse(CourierDto):
    rating: Optional[int32]
    earnings: Optional[int32]
