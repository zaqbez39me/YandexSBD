from datetime import date, datetime, time
from typing import Annotated, Optional

from fastapi import Depends, Path, Query

from app.api.dependencies.database import get_repository
from app.database.repositories.couriers import CouriersRepository
from app.schemas.models.common import int32, int64
from app.schemas.models.couriers import CourierDto
from app.schemas.models.orders import OrderDto, CouriersGroupOrders
from app.schemas.requests.couriers import CreateCourierRequest
from app.schemas.responses.couriers import GetCourierMetaInfoResponse


async def create_courier(
        create_courier_request: CreateCourierRequest,
        couriers_repo: CouriersRepository = Depends(get_repository(CouriersRepository))
) -> list[CourierDto]:
    return await couriers_repo.create_couriers(
        create_couriers=create_courier_request.__getattribute__("couriers")
    )


async def get_courier(
        courier_id: int64 = Path(description="Courier identifier"),
        couriers_repo: CouriersRepository = Depends(get_repository(CouriersRepository))
) -> CourierDto:
    return await couriers_repo.get_courier(courier_id=courier_id)


async def date_to_datetime_start(
        date_to_convert: date = Query(
            alias='startDate',
            description="Rating calculation start date",
            example="2023-01-20"
        )
) -> datetime:
    return datetime.combine(date_to_convert, time.min)


async def date_to_datetime_end(
        date_to_convert: date = Query(
            alias='endDate',
            description="Rating calculation end date",
            example="2023-01-21"
        )
) -> datetime:
    return datetime.combine(date_to_convert, time.min)


async def get_courier_metadata(
        courier: CourierDto = Depends(get_courier)
) -> GetCourierMetaInfoResponse:
    return GetCourierMetaInfoResponse(
        courier_type=courier.courier_type,
        regions=courier.regions,
        working_hours=courier.working_hours,
        courier_id=courier.courier_id
    )


async def get_couriers_assignments(
        date: Optional[Annotated[date, Query(
            alias='date',
            description="Дата распределения заказов. "
                        "Если не указана, то используется текущий день"
        )]] = date.today(),
        courier_id: Optional[Annotated[int64, Query(
            alias='courier_id',
            description="Идентификатор курьера для получения списка "
                        "распредленных заказов. Если не указан, возвращаются "
                        "данные по всем курьерам."
        )]] = None,
        couriers_repo: CouriersRepository = Depends(get_repository(CouriersRepository))
) -> list[CouriersGroupOrders]:
    return await couriers_repo.get_couriers_assignments(courier_id=courier_id, date=date)


async def get_courier_orders_in_time_interval(
        courier_id: int64 = Path(title="The ID of the courier"),
        start_date: datetime = Depends(date_to_datetime_start),
        end_date: datetime = Depends(date_to_datetime_end),
        couriers_repo: CouriersRepository = Depends(get_repository(CouriersRepository))
) -> list[OrderDto]:
    return await couriers_repo.get_courier_orders_in_time_interval(
        courier_id=courier_id,
        start_date=start_date,
        end_date=end_date
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
                    example=0
                )
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
                    example=10
                )
            ]
        ] = 1,
        couriers_repo: CouriersRepository = Depends(get_repository(CouriersRepository))
) -> list[CourierDto]:
    return await couriers_repo.get_couriers_in_range(limit=limit, offset=offset)
