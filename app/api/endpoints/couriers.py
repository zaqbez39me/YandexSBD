from datetime import date, datetime
from typing import Annotated, Optional

from fastapi import APIRouter, Depends
from fastapi.params import Query
from starlette import status

from app.api.dependencies.couriers import (
    create_courier_dependency, date_to_datetime_end_dependency,
    date_to_datetime_start_dependency, get_courier_dependency,
    get_courier_metadata_dependency,
    get_courier_orders_in_time_interval_dependency,
    get_couriers_assignments_dependency, get_couriers_in_range_dependency)
from app.schemas.models.common import int32
from app.schemas.models.couriers import CourierDto, CourierTypeEnum
from app.schemas.models.orders import CouriersGroupOrders, OrderDto
from app.schemas.responses.common import BadRequestResponse, NotFoundResponse
from app.schemas.responses.couriers import (CreateCouriersResponse,
                                            GetCourierMetaInfoResponse,
                                            GetCouriersResponse)
from app.schemas.responses.orders import OrderAssignResponse

courier_earning_coefficients = {
    CourierTypeEnum.foot: 2,
    CourierTypeEnum.bike: 3,
    CourierTypeEnum.auto: 4,
}

courier_rating_coefficients = {
    CourierTypeEnum.foot: 3,
    CourierTypeEnum.bike: 2,
    CourierTypeEnum.auto: 1,
}

router = APIRouter(tags=["courier-controller"], prefix="/couriers")


@router.post(
    "/",
    name="couriers::add-couriers",
    operation_id="createCourier",
    status_code=status.HTTP_200_OK,
    response_model=CreateCouriersResponse,
    responses={
        status.HTTP_200_OK: {
            "model": CreateCouriersResponse,
            "description": "ok",
        },
        status.HTTP_400_BAD_REQUEST: {
            "model": BadRequestResponse,
            "description": "bad request",
        },
    },
    tags=["courier-controller"],
)
async def add_couriers(
    couriers: list[CourierDto] = Depends(create_courier_dependency),
):
    return CreateCouriersResponse(couriers=couriers)


@router.get(
    "/assignments",
    summary="Список распределенных заказов",
    operation_id="couriersAssignments",
    name="couriers::get_couriers_assignments",
    status_code=status.HTTP_200_OK,
    response_model=OrderAssignResponse,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "model": BadRequestResponse,
            "description": "Order not found, assigned to another courier or not assigned at all",
        },
    },
    tags=["courier-controller"],
    response_model_exclude_none=True,
)
async def get_couriers_assignments(
    assignments_date: Optional[
        Annotated[
            date,
            Query(
                alias="date",
                description="Дата распределения заказов. "
                "Если не указана, то используется текущий день",
            ),
        ]
    ] = date.today(),
    couriers: list[CouriersGroupOrders] = Depends(
        get_couriers_assignments_dependency
    ),
):
    return OrderAssignResponse(date=assignments_date, couriers=couriers)


@router.get(
    "/{courier_id}",
    operation_id="getCourierById",
    name="couriers::get-courier-by-id",
    status_code=status.HTTP_200_OK,
    response_model=CourierDto,
    responses={
        status.HTTP_200_OK: {"model": CourierDto, "description": "ok"},
        status.HTTP_400_BAD_REQUEST: {
            "model": BadRequestResponse,
            "description": "bad request",
        },
        status.HTTP_404_NOT_FOUND: {
            "model": NotFoundResponse,
            "description": "not found",
        },
    },
    tags=["courier-controller"],
)
async def get_courier_by_id(
    courier: CourierDto = Depends(get_courier_dependency),
):
    return courier


@router.get(
    "/",
    name="couriers::get-couriers-in-range",
    operation_id="getCouriers",
    status_code=status.HTTP_200_OK,
    response_model=GetCouriersResponse,
    responses={
        status.HTTP_200_OK: {"model": GetCouriersResponse, "description": "ok"},
        status.HTTP_400_BAD_REQUEST: {
            "model": BadRequestResponse,
            "description": "bad request",
        },
    },
    tags=["courier-controller"],
)
async def get_couriers_in_range(
    offset: Optional[
        Annotated[
            int32,
            Query(
                title="Offset for the couriers",
                description="Максимальное количество курьеров в выдаче. "
                "Если параметр не передан, то значение по "
                "умолчанию равно 1.",
                ge=0,
                example=0,
            ),
        ]
    ] = 0,
    limit: Optional[
        Annotated[
            int32,
            Query(
                title="Limit for the couriers",
                description="Количество курьеров, которое нужно пропустить "
                "для отображения текущей страницы. Если параметр "
                "не передан, то значение по умолчанию равно 0.",
                ge=1,
                example=10,
            ),
        ]
    ] = 1,
    couriers: list[CourierDto] = Depends(get_couriers_in_range_dependency),
):
    return GetCouriersResponse(couriers=couriers, limit=limit, offset=offset)


@router.get(
    "/meta-info/{courier_id}",
    name="couriers::get_courier_meta_info",
    operation_id="getCourierMetaInfo",
    status_code=status.HTTP_200_OK,
    response_model=GetCourierMetaInfoResponse,
    responses={
        status.HTTP_200_OK: {
            "model": GetCourierMetaInfoResponse,
            "description": "OK",
        }
    },
    tags=["courier-controller"],
    response_model_exclude_unset=True,
)
async def get_courier_meta_info(
    courier_meta_info: GetCourierMetaInfoResponse = Depends(
        get_courier_metadata_dependency
    ),
    start_date: datetime = Depends(date_to_datetime_start_dependency),
    end_date: datetime = Depends(date_to_datetime_end_dependency),
    orders: list[OrderDto] = Depends(
        get_courier_orders_in_time_interval_dependency
    ),
):

    """
    Gets the metadata for a courier.

    Parameters:
        * courier_meta_info: GetCourierMeta
        * courier_id: The ID of the courier to get metadata for.
        * start_date: The start date of the time interval.
        * end_date: The end date of the time interval.
        * orders: The list of orders for the courier in the specified time interval.

    Returns:

        * A `GetCourierMetaInfoResponse` object containing the courier's metadata.

    """

    if orders:
        courier_type = CourierTypeEnum(courier_meta_info.courier_type)
        earning_coefficient = courier_earning_coefficients[courier_type]
        rating_coefficient = courier_rating_coefficients[courier_type]
        courier_meta_info.earnings = 0
        hours = ((end_date - start_date).total_seconds()) // 3600
        courier_meta_info.rating = round(
            len(orders) / hours * rating_coefficient
        )
        for order in orders:
            courier_meta_info.earnings += order.cost
        courier_meta_info.earnings *= earning_coefficient
    return courier_meta_info
