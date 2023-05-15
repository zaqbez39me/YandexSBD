from fastapi import APIRouter, Depends
from starlette import status

from app.api.dependencies.orders import (add_orders, complete_order,
                                         get_order_by_id, get_orders_in_range)
from app.schemas.models.orders import OrderDto
from app.schemas.responses.common import BadRequestResponse, NotFoundResponse

router = APIRouter(tags=["order-controller"], prefix="/orders")


@router.get(
    "/",
    name="orders::get-orders-in-range",
    operation_id="getOrders",
    status_code=status.HTTP_200_OK,
    response_model=list[OrderDto],
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "model": BadRequestResponse,
            "description": "bad request",
        },
    },
    tags=["order-controller"],
    response_model_exclude_none=True,
)
async def get_orders_in_range(
    orders: list[OrderDto] = Depends(get_orders_in_range),
):
    return orders


@router.get(
    "/{order_id}",
    name="orders::get-order-by-id",
    operation_id="getOrder",
    status_code=status.HTTP_200_OK,
    response_model=OrderDto,
    responses={
        status.HTTP_200_OK: {"model": OrderDto, "description": "ok"},
        status.HTTP_400_BAD_REQUEST: {
            "model": BadRequestResponse,
            "description": "bad request",
        },
        status.HTTP_404_NOT_FOUND: {
            "model": NotFoundResponse,
            "description": "not found",
        },
    },
    tags=["order-controller"],
    response_model_exclude_none=True,
)
async def get_order_by_id(order: OrderDto = Depends(get_order_by_id)):
    return order


@router.post(
    "/",
    name="orders::add-orders",
    operation_id="createOrder",
    status_code=status.HTTP_200_OK,
    response_model=list[OrderDto],
    responses={
        "400": {"description": "bad request", "model": BadRequestResponse},
    },
    tags=["order-controller"],
    response_model_exclude_none=True,
)
async def add_orders(orders_dto: list[OrderDto] = Depends(add_orders)):
    return orders_dto


@router.post(
    "/complete",
    name="orders::complete-order",
    operation_id="completeOrder",
    status_code=status.HTTP_200_OK,
    description="Завершить заказ, если каждый из них не завершен, существует "
    "в базе данных, а идентификатор курьера каждого заказа равен "
    "идентификатору курьера в запросе",
    response_model=list[OrderDto],
    responses={
        status.HTTP_200_OK: {
            "model": OrderDto,
            "description": "Заказ успешно завершен",
        },
        status.HTTP_400_BAD_REQUEST: {
            "model": BadRequestResponse,
            "description": "Заказ не найден, назначен на другого курьера или не назначен вовсе",
        },
    },
    tags=["order-controller"],
    response_model_exclude_none=True,
)
async def complete_order(
    completed_orders: list[OrderDto] = Depends(complete_order),
):
    return completed_orders
