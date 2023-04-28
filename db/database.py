""" Creates a simple sqlalchemy connection to a mysql database using sessions """
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base


# Database config
Base = declarative_base()
engine = create_async_engine(f'sqlite+aiosqlite:///db/taskbot.db', echo=True)
async_session = async_sessionmaker(bind=engine)
