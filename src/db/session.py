import os 
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from src.models.db_model import Base
from sqlalchemy.dialects.postgresql import insert
from src.models.db_model import CampgroundDB
from sqlalchemy.inspection import inspect


#load .env
load_dotenv()

#read link address
DATABASE_URL = os.getenv("DB_URL")

#creat async engine
engine = create_async_engine(DATABASE_URL, echo=True)

#session factory 
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

#to create tables
async def init_db():
    from src.models.db_model import Base
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


def obj_to_dict(obj):
    return {c.key: getattr(obj, c.key) for c in inspect(obj).mapper.column_attrs}


async def save_campgrounds_to_db(campgrounds: list[CampgroundDB], session: AsyncSession):
    for cg in campgrounds:
        data = obj_to_dict(cg)
        stmt = insert(CampgroundDB).values(**data)
        stmt = stmt.on_conflict_do_update(
            index_elements=['id'],
            set_=data
        )
        await session.execute(stmt)
    await session.commit()