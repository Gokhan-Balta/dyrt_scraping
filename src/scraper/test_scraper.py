import asyncio
from src.scraper.dyrt_scraper import fetch_and_save

if __name__ == "__main__":
    asyncio.run(fetch_and_save())