""" Contains the schemas for the sqlite database """
from sqlalchemy import Integer, String, Column
from database import Base, engine


class Tasks(Base):
    """ Represents a task  """
    __tablename__ = 'tasks'

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    discord_user_id = Column("discord_user_id", Integer)
    insertion_date = Column("insertion_date", String)
    due_date = Column("due_date", String)
    content = Column("content", String)

    def __init__(self, discord_user_id: int, insertion_date: str, due_date: str, content: str, id: int = None):
        self.id = id
        self.discord_user_id = discord_user_id
        self.insertion_date = insertion_date
        self.due_date = due_date
        self.content = content

    def __repr__(self):
        return f"{self.id} {self.discord_user_id} {self.insertion_date} {self.due_date} {self.content}"


class Configs(Base):
    """ Keeps the configuration for the discord server """
    __tablename__ = 'configs'

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    guild_id = Column("guild_id", Integer, unique=True)
    tasks_channel_id = Column("tasks_channel_id", Integer)

    def __init__(self, guild_id: int, tasks_channel_id: int, id: int = None):
        self.id = id
        self.guild_id = guild_id
        self.tasks_channel_id = tasks_channel_id

    def __repr__(self):
        return f"{self.id} {self.guild_id} {self.tasks_channel_id}"


def create_all_tables():
    Base.metadata.create_all(bind=engine)
