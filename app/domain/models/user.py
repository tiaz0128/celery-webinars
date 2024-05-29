from sqlalchemy.sql import func
from sqlalchemy import Column, CHAR, TIMESTAMP, VARCHAR

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class UserMst(Base):
    __tablename__ = "user_mst"

    parent_id = Column(CHAR(128), primary_key=True)
    user_id = Column(CHAR(128), primary_key=True, unique=True)

    ins_dt = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=func.UTC_TIMESTAMP()
    )
    ins_user = Column(VARCHAR(128), nullable=False)

    upd_dt = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=func.UTC_TIMESTAMP()
    )
    upd_user = Column(VARCHAR(128), nullable=False)
