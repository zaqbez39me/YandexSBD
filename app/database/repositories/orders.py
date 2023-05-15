from datetime import datetime

from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.sql.operators import eq, lt, ge

from app.database.error import NotFoundInDBError, ConflictWithRequestDBError
from app.database.models.assignment import AssignmentDB
from app.database.models.order import OrderDB
from app.database.repositories.base import BaseRepository
from app.schemas.models.orders import OrderDto, CreateOrderDto, CompleteOrder


class OrdersRepository(BaseRepository):
    def __init__(self, conn: AsyncSession) -> None:
        super().__init__(conn)

    async def get_order_by_order_id(self, *, order_id: int) -> OrderDto:
        result: Result = await self.connection.execute(select(OrderDB).where(eq(OrderDB.order_id, order_id)))
        order_row = result.scalars().one_or_none()
        if order_row:
            return await self._get_order_from_db_row(order_row)
        raise NotFoundInDBError(message=f"Order {order_id} not found in database")

    async def get_orders_in_range(self, *, limit: int, offset: int) -> list[OrderDto]:
        result: Result = await self.connection.execute(select(OrderDB).offset(offset).limit(limit))
        order_rows = result.scalars().all()
        orders = [
            await self._get_order_from_db_row(order_row) for order_row in order_rows
        ]
        return orders

    async def get_orders_in_time_interval(
            self,
            *,
            courier_id: int,
            start_date: datetime,
            end_date: datetime
    ) -> list[OrderDto]:
        result: Result = await self.connection.execute(
            select(OrderDB).where(
                eq(OrderDB.courier_id, courier_id),
                lt(OrderDB.complete_time, end_date),
                ge(OrderDB.complete_time, start_date)
            )
        )
        order_rows = result.scalars().all()
        orders: list[OrderDto] = [
            await self._get_order_from_db_row(order_row) for order_row in order_rows
        ]
        return orders

    async def add_orders(self, *, orders: list[CreateOrderDto]) -> list[OrderDto]:
        orders_dto = []
        for order in orders:
            order_row: OrderDB = await self._get_db_row_from_create_order(order)
            self.connection.add(order_row)
            await self.connection.commit()
            await self.connection.refresh(order_row)
            orders_dto.append(await self._get_order_from_db_row(order_row))
        return orders_dto

    async def complete_orders(self, *, complete_orders: list[CompleteOrder]) -> list[OrderDto]:
        complete_orders_result = []
        # Получить ID для всех заказов, которые следует завершить
        complete_orders_ids = (complete_order.order_id for complete_order in complete_orders)
        # Извлечь из базы данных записи с соответсвующими ID
        complete_orders_db_rows: Result = await self.connection.execute(
            select(OrderDB).where(
                OrderDB.order_id.in_(complete_orders_ids)
            ).options(
                selectinload(OrderDB.assignments)
            )
        )
        # Записать все ID в словарь для быстрого доступа при проходе по заказам
        # из запроса
        complete_orders_db_rows_dict: dict[int, OrderDB] = {
            row.order_id: row for row in complete_orders_db_rows.scalars() if row
        }
        # Пройтись по всем заказам из запроса
        for order in complete_orders:
            # Безопасно извлечь заказ из словаря
            order_row: OrderDB = complete_orders_db_rows_dict.get(order.order_id)
            # Вывести ошибку, если заказ не найден в базе данных
            if not order_row:
                raise NotFoundInDBError(
                    message=f"Order {order.order_id} not found in database"
                )
            # Проверить что заказ не завершен и заказ из запроса имеет время
            # для завершения. В случае несоответсвия вызвать исключение
            if order_row.complete_time or not order.complete_time:
                raise ConflictWithRequestDBError(
                    message=f"Order {order.order_id} is conflicting with database"
                )
            # Получить назначение соответствующее дате заказа
            order_assignment = await self._get_assignment_by_date(order_row, order.complete_time)
            # Проверить назначение на валидность
            if not order_assignment or order_assignment.courier_id != order.courier_id:
                raise ConflictWithRequestDBError(
                    message=f"Order {order.order_id} is conflicting with database"
                )
            # Обновить время завершения у заказа в базе данных и id курьера завершившего заказ
            order_row.complete_time = order.complete_time
            order_row.courier_id = order.courier_id
            # Добавить заказ приведенных к модели OrderDto в список результатов
            complete_orders_result.append(await self._get_order_from_db_row(order_row))
        # Применить все изменения
        await self.connection.commit()
        # Вернуть список резульататов
        return complete_orders_result

    @staticmethod
    async def _get_assignment_by_date(order_row: OrderDB, complete_time: datetime) -> AssignmentDB | None:
        # Извлечь дату из datetime
        date = complete_time.date()
        # Пройтись циклом по всем назначениям связвнным с данным заказом
        for assignment in order_row.assignments:
            # Вернуть назначение, если дата соответсвует данной
            if assignment.assignment_date == date:
                return assignment


    @staticmethod
    async def _get_order_from_db_row(order_row) -> OrderDto:
        # Преобразовать запись заказа из БД в OrderDto схему
        return OrderDto(
            weight=order_row.weight,
            regions=order_row.regions,
            delivery_hours=order_row.delivery_hours,
            cost=order_row.cost,
            order_id=order_row.order_id,
            completed_time=order_row.complete_time
        )

    @staticmethod
    async def _get_db_row_from_create_order(create_order) -> OrderDB:
        # Преобразовать схему создания заказа в запись для БД
        return OrderDB(
            weight=create_order.weight,
            regions=create_order.regions,
            delivery_hours=create_order.delivery_hours,
            cost=create_order.cost
        )
