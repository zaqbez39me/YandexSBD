from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.schemas.models.common import int32, int32, int64, HoursList


class CreateOrderDto(BaseModel):
    weight: float
    regions: int32
    delivery_hours: HoursList
    cost: int32


class OrderDto(CreateOrderDto):
    order_id: int64
    completed_time: Optional[datetime] = None


class CompleteOrder(BaseModel):
    courier_id: int64
    order_id: int64
    complete_time: datetime


class GroupOrders(BaseModel):
    group_order_id: int64 | None
    orders: list[OrderDto]


class CouriersGroupOrders(BaseModel):
    courier_id: int64
    orders: list[GroupOrders]
