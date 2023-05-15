from datetime import date

from pydantic import BaseModel

from app.schemas.models.orders import CouriersGroupOrders


class OrderAssignResponse(BaseModel):
    date: date
    couriers: list[CouriersGroupOrders]
