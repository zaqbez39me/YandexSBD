from collections import defaultdict
from datetime import datetime

from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.operators import eq, and_

from app.database.error import NotFoundInDBError
from app.database.models.assignment import AssignmentDB
from app.database.models.assignment_order import assignment_order_table
from app.database.models.courier import CourierDB
from app.database.models.order import OrderDB
from app.database.repositories.base import BaseRepository
from app.database.repositories.orders import OrdersRepository
from app.schemas.models.couriers import CourierDto, CreateCourierDto
from app.schemas.models.orders import OrderDto, GroupOrders, CouriersGroupOrders


class CouriersRepository(BaseRepository):
    def __init__(self, conn: AsyncSession) -> None:
        super().__init__(conn)
        self._orders_repo = OrdersRepository(conn)

    async def create_couriers(self, *, create_couriers: list[CreateCourierDto]) -> list[CourierDto]:
        couriers_dto = []
        for courier in create_couriers:
            new_courier: CourierDB = await self._get_db_row_from_courier_create(courier)
            self.connection.add(new_courier)
            await self.connection.commit()
            await self.connection.refresh(new_courier)
            couriers_dto.append(await self._get_courier_from_db_row(new_courier))
        return couriers_dto

    async def get_courier(self, *, courier_id: int) -> CourierDto:
        result: Result = await self.connection.execute(
            select(CourierDB).where(eq(CourierDB.courier_id, courier_id))
        )
        courier_row: CourierDB | None = result.scalars().one_or_none()
        if not courier_row:
            raise NotFoundInDBError(
                message=f"Courier {courier_id} not found in database"
            )
        courier: CourierDto = await self._get_courier_from_db_row(courier_row)
        return courier

    async def get_couriers_in_range(self, *, limit: int, offset: int) -> list[CourierDto]:
        result: Result = await self.connection.execute(
            select(CourierDB).offset(offset).limit(limit)
        )
        courier_rows = result.scalars().all()
        orders = [
            await self._get_courier_from_db_row(order_row) for order_row in courier_rows
        ]
        return orders

    async def get_courier_orders_in_time_interval(
            self,
            *,
            courier_id: int,
            start_date: datetime,
            end_date: datetime
    ) -> list[OrderDto]:
        return await self._orders_repo.get_orders_in_time_interval(
            courier_id=courier_id,
            start_date=start_date,
            end_date=end_date
        )

    async def get_couriers_assignments(
            self,
            date: datetime.date,
            courier_id: int | None
    ):
        # Join orders with assignments where date is correct and select OrderDB
        query = select(OrderDB).select_from(
            assignment_order_table
            .join(OrderDB)
            .join(AssignmentDB, onclause=eq(AssignmentDB.assignment_date, date))
        )
        # Where clause to take courier with given id if given
        where_conditions = [
            eq(OrderDB.complete_time, None)
        ]
        if courier_id:
            where_conditions.append(eq(OrderDB.courier_id, courier_id))
        query = query.where(
            *where_conditions
        )
        # Execute the query
        result: Result = await self.connection.execute(
            query
        )
        # Fetch all scalars from the result to get orders and assignments
        order_rows = result.scalars().all()
        courier_assignments_dict = {}
        # Save the courier assignments hierarchy in dictionary
        for order in order_rows:
            if order.courier_id not in courier_assignments_dict:
                courier_assignments_dict[order.courier_id] = defaultdict(list)
            courier_assignments_dict[order.courier_id][order.group_order_id].append(order)
        courier_assignments = []
        for courier_id_key, group_orders_value in courier_assignments_dict.items():
            orders = []
            for group_order_id, group_orders in group_orders_value.items():
                group_orders_list = []
                for order in group_orders:
                    order_dto = OrderDto(
                        weight=order.weight,
                        regions=order.regions,
                        delivery_hours=order.delivery_hours,
                        cost=order.cost,
                        order_id=order.order_id,
                        completed_time=order.complete_time
                    )
                    group_orders_list.append(order_dto)
                orders.append(
                    GroupOrders(
                        group_order_id=group_order_id,
                        orders=group_orders_list
                    )
                )
            courier_assignments.append(
                CouriersGroupOrders(
                    courier_id=courier_id_key,
                    orders=orders
                )
            )
        return courier_assignments


    @staticmethod
    async def _get_courier_from_db_row(courier: CourierDB) -> CourierDto:
        return CourierDto(
            courier_type=courier.courier_type,
            regions=courier.regions,
            working_hours=courier.working_hours,
            courier_id=courier.courier_id
        )

    @staticmethod
    async def _get_db_row_from_courier_create(create_courier: CreateCourierDto) -> CourierDB:
        return CourierDB(
            courier_type=create_courier.courier_type,
            regions=create_courier.regions,
            working_hours=create_courier.working_hours
        )
