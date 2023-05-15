"""
This module provides a `AssignmentDB` class for representing assignments in the database.

The `AssignmentDB` class has the following attributes:

* `assignment_id`: The ID of the assignment.
* `assignment_date`: The date of the assignment.
* `courier_id`: The ID of the courier assigned to the assignment.
* `orders`: A list of orders assigned to the assignment.
* `courier`: The courier assigned to the assignment.
"""

from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import BIGINT, DATE
from sqlalchemy.orm import relationship

from app.database.base import Base
from app.database.models.assignment_order import assignment_order_table


class AssignmentDB(Base):
    """
    A class representing an assignment in the database.

    Attributes:
        `assignment_id`: The ID of the assignment.
        `assignment_date`: The date of the assignment.
        `courier_id`: The ID of the courier assigned to the assignment.
        `orders`: A list of orders assigned to the assignment.
        `courier`: The courier assigned to the assignment.

    """

    __tablename__ = "assignment"
    assignment_id = Column(
        "assignment_id",
        BIGINT,
        primary_key=True,
        nullable=False,
        autoincrement=True,
        index=True,
    )
    assignment_date = Column(
        "assignment_date", DATE, index=True, nullable=False
    )
    courier_id = Column(
        "courier_id", BIGINT, ForeignKey("courier.courier_id"), nullable=False
    )
    orders = relationship(
        "OrderDB",
        secondary=assignment_order_table,
        back_populates="assignments",
    )
    courier = relationship("CourierDB", back_populates="assignments")
