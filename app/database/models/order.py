from sqlalchemy import Column, FLOAT, CheckConstraint
from sqlalchemy.dialects.postgresql import CHAR, ARRAY, INTEGER, BIGINT, TIMESTAMP
from sqlalchemy.orm import relationship

from app.database.base import Base
from app.database.models.assignment_order import assignment_order_table


class OrderDB(Base):
    __tablename__ = 'order'
    order_id = Column("order_id", BIGINT, primary_key=True,
                      unique=True, autoincrement=True, index=True)
    weight = Column("weight", FLOAT, CheckConstraint("weight>=0"))
    delivery_hours = Column("delivery_hours", ARRAY(CHAR(11)))
    regions = Column("regions", INTEGER, CheckConstraint("regions>0"))
    cost = Column("cost", INTEGER, CheckConstraint("cost>0"))
    complete_time = Column("complete_time", TIMESTAMP(timezone=True), nullable=True)
    courier_id = Column("courier_id", BIGINT, nullable=True, default=None)
    group_order_id = Column("group_order_id", BIGINT, nullable=True, default=None, index=True)
    assignments = relationship("AssignmentDB",
                               secondary=assignment_order_table, back_populates="orders")
