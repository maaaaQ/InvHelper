import datetime
from uuid import UUID
from pydantic import BaseModel, Field
from app.enums import FilterDividendPolicy, FilterOccupation


class StockBase(BaseModel):
    title: str = Field(title="Название компании")
    stock_symbol: str = Field(title="Тикер акции")
    description: str = Field(title="Описание компании")
    capitalization: int = Field(title="Капитализация компании")
    dividend_policy: FilterDividendPolicy = Field(
        title="Выплата дивидендов", default=FilterDividendPolicy.NO_DIVIDEND
    )
    occupation: FilterOccupation = Field(
        title="Вид деятельности компании", default_factory=None
    )
    created_at: datetime.datetime = Field(
        title="Дата покупки акции", default=datetime.datetime.utcnow
    )
    user_id: UUID = Field(title="Идентификатор пользователя")

    class Config:
        from_attributes = True


class StockOn(StockBase):
    pass


class Stock(StockBase):
    id: int = Field(title="Идентификатор акции", default=None)
