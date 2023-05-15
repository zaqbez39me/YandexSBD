from sqlalchemy import CheckConstraint, Column
from sqlalchemy.dialects.postgresql import ARRAY, BIGINT, CHAR, INTEGER
from sqlalchemy.orm import relationship

from app.database.base import Base


class CourierDB(Base):
    __tablename__ = "courier"
    courier_id = Column(
        "courier_id",
        BIGINT,
        unique=True,
        primary_key=True,
        autoincrement=True,
        index=True,
    )
    courier_type = Column("courier_type", CHAR(4))
    regions = Column(
        "regions", ARRAY(INTEGER), CheckConstraint("0 < ALL(regions)")
    )
    working_hours = Column("working_hours", ARRAY(CHAR(11)))
    assignments = relationship("AssignmentDB", back_populates="courier")
