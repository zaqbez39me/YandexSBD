from pydantic import BaseModel

from app.schemas.models.orders import CompleteOrder, CreateOrderDto


class CreateOrderRequest(BaseModel):
    orders: list[CreateOrderDto]


class CompleteOrderRequestDto(BaseModel):
    complete_info: list[CompleteOrder]
