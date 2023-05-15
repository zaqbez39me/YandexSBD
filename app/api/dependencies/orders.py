"""
This module contains the dependencies for the orders API.

The dependencies in this module are used to access the database and to perform CRUD operations on orders.

The following dependencies are defined in this module:

* `get_order_by_id`: Gets an order by ID.
* `get_orders_in_range`: Gets a list of orders, paginated by offset and limit.
* `add_orders`: Creates new orders.
* `get_completed_orders`: Gets a list of completed orders.
* `complete_order`: Marks an order as completed.

"""

from typing import Annotated, Optional

from fastapi import Depends, Path, Query

from app.api.dependencies.database import get_repository
from app.database.repositories.orders import OrdersRepository
from app.schemas.models.common import int32, int64
from app.schemas.models.orders import OrderDto
from app.schemas.requests.orders import (CompleteOrderRequestDto,
                                         CreateOrderRequest)


async def get_order_by_id(
    order_id: Annotated[int64, Path(description="Order identifier")],
    orders_repo: OrdersRepository = Depends(get_repository(OrdersRepository)),
) -> OrderDto:
    """
    Gets an order by ID.

    Parameters:

        * order_id: The ID of the order to get.
        * orders_repo: The repository that stores the orders.

    Returns:

        * An `OrderDto` object representing the order.
    """

    return await orders_repo.get_order_by_order_id(order_id=order_id)


async def get_orders_in_range(
    limit: Optional[
        Annotated[
            int,
            Query(
                title="Максимальное количество заказов в выдаче. "
                "Если параметр не передан, то значение по умолчанию равно 1.",
                ge=1,
                example=10,
            ),
        ]
    ] = 1,
    offset: Optional[
        Annotated[
            int32,
            Query(
                title="Количество заказов, которое нужно пропустить для отображения "
                "текущей страницы. Если параметр не передан, то значение по "
                "умолчанию равно 0.",
                ge=0,
                example=0,
            ),
        ]
    ] = 0,
    orders_repo: OrdersRepository = Depends(get_repository(OrdersRepository)),
) -> list[OrderDto]:
    """
    Gets a list of orders, paginated by offset and limit.

    Parameters:

        * offset: The offset to start at.
        * limit: The number of orders to return.
        * orders_repo: The repository that stores the orders.

    Returns:

        * A list of `OrderDto` objects, each representing an order.

    """

    return await orders_repo.get_orders_in_range(offset=offset, limit=limit)


async def add_orders(
    create_order_request: CreateOrderRequest,
    orders_repo: OrdersRepository = Depends(get_repository(OrdersRepository)),
) -> list[OrderDto]:
    """
    Creates new orders.

    Parameters:

        * create_order_request: The request object containing the orders' details.
        * orders_repo: The repository that stores the orders.

    Returns:

        * A list of `OrderDto` objects, each representing the created order.

    """

    return await orders_repo.add_orders(orders=create_order_request.orders)


async def get_completed_orders(
    complete_order_request: CompleteOrderRequestDto,
    orders_repo: OrdersRepository = Depends(get_repository(OrdersRepository)),
) -> list[OrderDto]:
    """
    Gets a list of completed orders.

    Parameters:

        * complete_order_request: The request object containing the completed orders' details.
        * orders_repo: The repository that stores the orders.

    Returns:

        * A list of `OrderDto` objects, each representing a completed order.

    """

    return await orders_repo.complete_orders(
        complete_orders=complete_order_request.complete_info
    )


async def complete_order(
    completed_orders: list[OrderDto] = Depends(get_completed_orders),
) -> list[OrderDto]:
    """
    Marks an order as completed.

    Parameters:

        * completed_orders: The list of orders to mark as completed.
        * orders_repo: The repository that stores the orders.

    Returns:

        * A list of `OrderDto` objects, each representing the completed order.

    """

    return completed_orders
