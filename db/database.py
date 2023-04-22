from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker


# Database config
Base = declarative_base()
engine = create_engine(f'sqlite:///db/taskbot.db', echo=True)

Session = sessionmaker(bind=engine)
session = Session()
