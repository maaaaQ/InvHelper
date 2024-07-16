import logging
from sqlalchemy.orm import Session

from . import config, crud
from .database.database import DB_INITIALIZER
from .schemas import StockOn, Stock
from .enums import FilterDividendPolicy, FilterOccupation
import typing
from fastapi import Depends, FastAPI, Header, Query
from fastapi.responses import JSONResponse


logger = logging.getLogger(__name__)
logging.basicConfig(level=2, format="%(levelname)-9s %(message)s")


cfg: config.Config = config.load_config()

# Загрузка конфигурации
logger.info(
    "Service configuration loaded:\n"
    + f"{cfg.model_dump_json(by_alias=True, indent=4)}"
)

# Инициализация базы данных
logger.info("Initializing database...")
SessionLocal = DB_INITIALIZER.init_database(str(cfg.postgres_dsn))


app = FastAPI(title="INVHelper API")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get(
    "/stocks",
    summary="Возвращает список акций",
    response_model=list[Stock],
    tags=["stocks"],
)
async def get_stocks_list(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    dividend_policy: FilterDividendPolicy | None = None,
    occupation: FilterOccupation | None = None,
) -> typing.List[Stock]:
    return crud.get_stocks(db, skip, limit, dividend_policy, occupation)


@app.get("/stocks/{stocks_id}", summary="Возвращает акцию по ее ID", tags=["stocks"])
async def get_stocks_by_id(stocks_id: int, db: Session = Depends(get_db)) -> Stock:
    stocks = crud.get_info_about_stocks(db, stocks_id)
    if stocks != None:
        return stocks
    return JSONResponse(
        status_code=404, content={"message": "Акция не найдена вашем портфеле"}
    )


@app.get(
    "/stocks/{stock_symbol}", summary="Возвращает акцию по ее тикеру", tags=["stocks"]
)
async def get_stocks_by_tiker(
    stock_symbol: int, db: Session = Depends(get_db)
) -> Stock:
    stocks = crud.get_info_about_stocks(db, stock_symbol)
    if stocks != None:
        return stocks
    return JSONResponse(
        status_code=404, content={"message": "Акция не найдена вашем портфеле"}
    )


@app.post(
    "/stock",
    status_code=201,
    summary="Создает новую акцию",
    response_model=Stock,
    tags=["stocks"],
)
async def add_stock(stocks: StockOn, db: Session = Depends(get_db)) -> Stock:
    stocks = crud.create_stocks(db, stocks)
    if stocks != None:
        messages = {
            "id": str(stocks.id),
            "title": str(stocks.title),
            "stock_symbol": str(stocks.stock_symbol),
            "description": str(stocks.description),
            "capitalization": str(stocks.capitalization),
            "dividend_policy": str(stocks.dividend_policy),
            "occupation": str(stocks.occupation),
            "created_at": str(stocks.created_at),
            "user_id": str(stocks.user_id),
        }
        return stocks


@app.put("/stocks/{stocks_id}", summary="Обновляет акцию по ее ID", tags=["stocks"])
async def update_stocks(
    stocks_id: int, stocks: StockOn, db: Session = Depends(get_db)
) -> Stock:
    stocks = crud.get_info_about_stocks(db, stocks_id, stocks)
    if stocks != None:
        return stocks
    return JSONResponse(status_code=404, content={"message": "Акция не найдена"})


@app.delete("/stocks/{stocks_id}", summary="Удаляет акцию по ее ID", tags=["stocks"])
async def delete_stocks_by_id(stocks_id: int, db: Session = Depends(get_db)) -> Stock:
    if crud.delete_stocks(db, stocks_id):
        return JSONResponse(
            status_code=200, content={"message": "Акция успешно удалена"}
        )
    return JSONResponse(
        status_code=404, content={"message": "По данному ID акция не найдена "}
    )
