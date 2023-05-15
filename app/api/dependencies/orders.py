from typing import Annotated, Optional

from fastapi import Depends, Path, Query

from app.api.dependencies.database import get_repository
from app.database.repositories.orders import OrdersRepository
from app.schemas.models.common import int32, int64
from app.schemas.models.orders import OrderDto
from app.schemas.requests.orders import CreateOrderRequest, CompleteOrderRequestDto


async def get_order_by_id(
        order_id: Annotated[
            int64,
            Path(description="Order identifier")
        ],
        orders_repo: OrdersRepository = Depends(get_repository(OrdersRepository))
) -> OrderDto:
    return await orders_repo.get_order_by_order_id(order_id=order_id)


async def get_orders_in_range(
        limit: Optional[
            Annotated[
                int,
                Query(
                    title="Максимальное количество заказов в выдаче. "
                          "Если параметр не передан, то значение по умолчанию равно 1.",
                    ge=1,
                    example=10
                )]
        ] = 1,
        offset: Optional[
            Annotated[
                int32,
                Query(
                    title="Количество заказов, которое нужно пропустить для отображения "
                          "текущей страницы. Если параметр не передан, то значение по "
                          "умолчанию равно 0.",
                    ge=0,
                    example=0
                )
            ]
        ] = 0,
        orders_repo: OrdersRepository = Depends(get_repository(OrdersRepository))
) -> list[OrderDto]:
    return await orders_repo.get_orders_in_range(offset=offset, limit=limit)


async def add_orders(
        create_order_request: CreateOrderRequest,
        orders_repo: OrdersRepository = Depends(get_repository(OrdersRepository))
) -> list[OrderDto]:
    return await orders_repo.add_orders(orders=create_order_request.orders)


async def get_completed_orders(
        complete_order_request: CompleteOrderRequestDto,
        orders_repo: OrdersRepository = Depends(get_repository(OrdersRepository))
) -> list[OrderDto]:
    return await orders_repo.complete_orders(complete_orders=complete_order_request.complete_info)


async def complete_order(
        completed_orders: list[OrderDto] = Depends(get_completed_orders)
) -> list[OrderDto]:
    return completed_orders
