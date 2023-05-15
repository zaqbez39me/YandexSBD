from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.dialects.postgresql import BIGINT

from app.database.base import Base

assignment_order_table = Table(
    "assignment_order",
    Base.metadata,
    Column("order_id", BIGINT, ForeignKey("order.order_id")),
    Column("assignment_id", BIGINT, ForeignKey("assignment.assignment_id")),
)
