import logging
from fastapi import FastAPI
import aiohttp
import asyncio
import config

logger = logging.getLogger(__name__)
logging.basicConfig(level=2, format="%(levelname)-9s %(message)s")


cfg: config.Config = config.load_config()

logger.info(
    "Service configuration loaded:\n"
    + f"{cfg.model_dump_json(by_alias=True, indent=4)}"
)

app = FastAPI()


@app.get("/nowprice")
async def get_info_about_stocks(tiker: str):
    async with aiohttp.ClientSession() as session:
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={tiker}&interval=5min&apikey={cfg.apikey}"
        async with session.get(url) as response:
            data = await response.json()
            return data


async def main():
    result = await get_info_about_stocks()
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
