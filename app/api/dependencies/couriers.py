"""
This module contains the dependencies for the couriers API.

The dependencies in this module are used to access the database and to convert dates to `datetime` objects.

The following dependencies are defined in this module:

* `create_courier_dependency`: Creates a new courier.
* `get_courier_dependency`: Gets a courier by ID.
* `date_to_datetime_start_dependency`: Converts a date to a `datetime` object.
* `date_to_datetime_end_dependency`: Converts a date to a `datetime` object.
* `get_courier_metadata_dependency`: Gets the metadata for a courier.
* `get_couriers_assignments_dependency`: Gets the list of courier assignments for a given date.
* `get_courier_orders_in_time_interval_dependency`: Gets the list of orders for a given courier in a given time interval.
* `get_couriers_in_range_dependency`: Gets a list of couriers, paginated by offset and limit.
"""

from datetime import date, datetime, time
from typing import Annotated, Optional

from fastapi import Depends, Path, Query

from app.api.dependencies.database import get_repository
from app.database.repositories.couriers import CouriersRepository
from app.schemas.models.common import int32, int64
from app.schemas.models.couriers import CourierDto
from app.schemas.models.orders import CouriersGroupOrders, OrderDto
from app.schemas.requests.couriers import CreateCourierRequest
from app.schemas.responses.couriers import GetCourierMetaInfoResponse


async def create_courier_dependency(
    create_courier_request: CreateCourierRequest,
    couriers_repo: CouriersRepository = Depends(
        get_repository(CouriersRepository)
    ),
) -> list[CourierDto]:
    """
    Creates a new courier.

    Parameters:
        create_courier_request: The request object containing the courier's details.
        couriers_repo: The repository that stores the couriers.

    Returns:
        A list of `CourierDto` objects, each representing the created courier.
    """

    return await couriers_repo.create_couriers(
        create_couriers=create_courier_request.couriers
    )


async def get_courier_dependency(
    courier_id: int64 = Path(description="Courier identifier"),
    couriers_repo: CouriersRepository = Depends(
        get_repository(CouriersRepository)
    ),
) -> CourierDto:
    """
    Gets a courier by ID.

    Parameters:
        courier_id: The ID of the courier to get.
        couriers_repo: The repository that stores the couriers.

    Returns:
        A `CourierDto` object representing the courier.
    """

    return await couriers_repo.get_courier(courier_id=courier_id)


async def date_to_datetime_start_dependency(
    date_to_convert: date = Query(
        alias="startDate",
        description="Rating calculation start date",
        example="2023-01-20",
    )
) -> datetime:
    """
    Converts a date to a `datetime` object.

    Parameters:
        date_to_convert: The date to convert.

    Returns:
        A `datetime` object representing the converted date.
    """

    return datetime.combine(date_to_convert, time.min)


async def date_to_datetime_end_dependency(
    date_to_convert: date = Query(
        alias="endDate",
        description="Rating calculation end date",
        example="2023-01-21",
    )
) -> datetime:
    """
    Converts a date to a `datetime` object.

    Parameters:
        date_to_convert: The date to convert.

    Returns:
        A `datetime` object representing the converted date.
    """

    return datetime.combine(date_to_convert, time.min)


async def get_courier_metadata_dependency(
    courier: CourierDto = Depends(get_courier_dependency),
) -> GetCourierMetaInfoResponse:
    """
    Gets the metadata for a courier.

    Parameters:
        courier: The courier to get metadata for.

    Returns:
        A `GetCourierMetaInfoResponse` object containing the courier's metadata.
    """

    return GetCourierMetaInfoResponse(
        courier_type=courier.courier_type,
        regions=courier.regions,
        working_hours=courier.working_hours,
        courier_id=courier.courier_id,
    )


async def get_couriers_assignments_dependency(
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
    courier_id: Optional[
        Annotated[
            int64,
            Query(
                alias="courier_id",
                description="Идентификатор курьера для получения списка "
                "распредленных заказов. Если не указан, возвращаются "
                "данные по всем курьерам.",
            ),
        ]
    ] = None,
    couriers_repo: CouriersRepository = Depends(
        get_repository(CouriersRepository)
    ),
) -> list[CouriersGroupOrders]:
    """
    Gets the list of courier assignments for a given date.

    Parameters:
        assignments_date: The date for which to get the assignments. If not specified, the current day will be used.
        courier_id: The ID of the courier to get assignments for. If not specified, assignments for all couriers will be returned.
        couriers_repo: Repo dependency

    Returns:
        A list of `CouriersGroupOrders` objects, each representing a group of orders assigned to a single courier.
    """

    return await couriers_repo.get_couriers_assignments(
        courier_id=courier_id, date=assignments_date
    )


async def get_courier_orders_in_time_interval_dependency(
    courier_id: int64 = Path(title="The ID of the courier"),
    start_date: datetime = Depends(date_to_datetime_start_dependency),
    end_date: datetime = Depends(date_to_datetime_end_dependency),
    couriers_repo: CouriersRepository = Depends(
        get_repository(CouriersRepository)
    ),
) -> list[OrderDto]:
    """
    Gets the list of orders for a given courier in a given time interval.

    Parameters:
        courier_id: The ID of the courier to get orders for.
        start_date: The start date of the time interval.
        end_date: The end date of the time interval.
        couriers_repo: Repo dependency

    Returns:
        A list of `OrderDto` objects, each representing an order.
    """

    return await couriers_repo.get_courier_orders_in_time_interval(
        courier_id=courier_id, start_date=start_date, end_date=end_date
    )


async def get_couriers_in_range_dependency(
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
    couriers_repo: CouriersRepository = Depends(
        get_repository(CouriersRepository)
    ),
) -> list[CourierDto]:
    """
    Gets a list of couriers, paginated by offset and limit.

    Parameters:
        offset: The offset to start at.
        limit: The number of couriers to return.
        couriers_repo: Repo dependency

    Returns:
        A list of `CourierDto` objects, each representing a courier.
    """

    return await couriers_repo.get_couriers_in_range(limit=limit, offset=offset)
