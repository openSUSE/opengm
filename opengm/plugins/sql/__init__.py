from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from opengm import DATABASE_URL


def start(base):
    engine = create_async_engine(DATABASE_URL, echo=True)
    base.metadata.bind = engine
    # BASE.metadata.create_all(engine)
    return (
        scoped_session(
            sessionmaker(
                bind=engine,
                class_=AsyncSession,
                expire_on_commit=False,
                autoflush=False,
            )
        ),
        engine,
    )


BASE = declarative_base()
SESSION, engine = start(BASE)


async def create(eng):
    async with eng.begin() as conn:
        await conn.run_sync(BASE.metadata.create_all)


def get_objects():
    return BASE, SESSION, engine
