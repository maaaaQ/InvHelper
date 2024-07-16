import typing
from sqlalchemy.orm import Session
from .database import models
from . import schemas
from .enums import FilterDividendPolicy, FilterOccupation


def create_stocks(db: Session, stocks: schemas.StockOn) -> models.Stocks:
    """Добавление информации по новой акции"""
    db_stocks = models.Stocks(
        title=stocks.title,
        stock_symbol=stocks.stock_symbol,
        description=stocks.description,
        capitalization=stocks.capitalization,
        dividend_policy=stocks.dividend_policy,
        occupation=stocks.occupation,
        created_at=stocks.created_at,
        user_id=stocks.user_id,
    )
    db.add(db_stocks)
    db.commit()
    db.refresh(db_stocks)
    return db_stocks


def get_stocks(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    dividend_policy: FilterDividendPolicy | None = None,
    occupation: FilterOccupation | None = None,
) -> typing.List[models.Stocks]:
    """Получение информации по акциям"""
    query = db.query(models.Stocks)
    if dividend_policy and occupation:
        return query.filter(
            models.Stocks.dividend_policy == FilterDividendPolicy(dividend_policy)
        ).filter(models.Stocks.occupation == FilterOccupation(occupation))
    if dividend_policy:
        return query.filter(
            models.Stocks.dividend_policy == FilterDividendPolicy(dividend_policy)
        )
    if occupation:
        return query.filter(models.Stocks.occupation == FilterOccupation(occupation))
    return query.offset(skip).limit(limit).all()


def get_info_about_stocks(db: Session, stocks_id: int) -> models.Stocks:
    """Показ конкретной акции по идентификатору"""
    return db.query(models.Stocks).filter(models.Stocks.id == stocks_id).first()


def get_info_about_stocks_by_stock_symbol(
    db: Session, stock_symbol: int
) -> models.Stocks:
    """Показ конкретной акции по тикеру акции"""
    return (
        db.query(models.Stocks)
        .filter(models.Stocks.stock_symbol == stock_symbol)
        .first()
    )


def update_stocks_by_id(
    db: Session, stocks_id: int, stocks: schemas.StockOn
) -> models.Stocks:
    """Обновление информации акции по ID"""
    result = (
        db.query(models.Stocks)
        .filter(models.Stocks.id == stocks_id)
        .update(stocks.dict())
    )
    db.commit()

    if result == 1:
        return get_info_about_stocks(db, stocks_id)
    return None


def update_stocks_by_tiker(
    db: Session, stock_symbol: int, stocks: schemas.StockOn
) -> models.Stocks:
    """Обновление информации акции по тикеру"""
    result = (
        db.query(models.Stocks)
        .filter(models.Stocks.stock_symbol == stocks.stock_symbol)
        .update(stocks.dict())
    )
    db.commit()

    if result == 1:
        return get_info_about_stocks_by_stock_symbol(db, stock_symbol)
    return None


def delete_stocks(db: Session, stocks_id: int) -> bool:
    """Удаление акции по идентификатору"""
    result = db.query(models.Stocks).filter(models.Stocks.id == stocks_id).delete()
    db.commit()
    return result == 1
