import asyncio
from src.db.session import init_db

async def main():
    await init_db()

asyncio.run(main())
