from pydantic import BaseModel

from app.schemas.models.orders import CreateOrderDto, CompleteOrder


class CreateOrderRequest(BaseModel):
    orders: list[CreateOrderDto]


class CompleteOrderRequestDto(BaseModel):
    complete_info: list[CompleteOrder]
