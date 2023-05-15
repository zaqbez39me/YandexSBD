from enum import Enum
from typing import Optional

from pydantic import BaseModel

from app.schemas.models.common import int32, int64, HoursList


class CourierTypeEnum(str, Enum):
    foot = "FOOT"
    bike = "BIKE"
    auto = "AUTO"


class CreateCourierDto(BaseModel):
    courier_type: CourierTypeEnum
    regions: list[int32]
    working_hours: HoursList


class CourierDto(CreateCourierDto):
    courier_id: Optional[int64]
