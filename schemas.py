""" Contains the schemas for the sqlite database """
from sqlalchemy import Integer, String, Column
from database import Base


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
