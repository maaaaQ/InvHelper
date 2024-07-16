import uuid
from sqlalchemy import Column, Integer, String, TIMESTAMP, Enum
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID

from app.enums import FilterDividendPolicy, FilterOccupation
from .database import Base


class Stocks(Base):
    __tablename__ = "stocks"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(40), index=True, nullable=False)
    stock_symbol = Column(String(6), index=True, nullable=False)
    description = Column(String(255), index=True, nullable=False)
    capitalization = Column(Integer, index=True, nullable=False)
    dividend_policy = Column(
        Enum(FilterDividendPolicy),
        index=True,
        nullable=False,
        default=FilterDividendPolicy.NO_DIVIDEND,
    )
    occupation = Column(
        Enum(FilterOccupation),
        index=True,
        nullable=False,
        default=FilterOccupation.OTHERS,
    )

    created_at = Column(TIMESTAMP, default=datetime.utcnow, index=True, nullable=False)
    user_id = Column(UUID(as_uuid=True), default=uuid.uuid4, index=True, nullable=False)
