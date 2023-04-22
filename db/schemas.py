""" Contains the schemas for the TaskBot's sqlite database """
from sqlalchemy import ForeignKey, Integer, String, Column, Boolean
from db.database import Base, engine


class Users(Base):
    """ Keeps the id of a Discord user """
    __tablename__ = 'users'

    id = Column("id", Integer, primary_key=True, autoincrement=False)
    def __init__(self, id: int):
        self.id = id
    
    def __repr__(self):
        return f"User -> id:{self.id}"


class Tasks(Base):
    """ Represents a task """
    __tablename__ = 'tasks'

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    title = Column("title", String)
    description = Column("description", String)
    inserted_at = Column("inserted_at", String)
    publish_at = Column("publish_at", String)
    has_been_sent = Column("has_been_sent", Boolean)
    task_message_id = Column("task_message_id", Integer, unique=True)
    id_creator = Column("id_creator", ForeignKey("users.id"))

    def __init__(
            self, title, description, inserted_at, publish_at, has_been_sent, 
            task_message_id, id_creator, id = None,
        ) -> None:
        self.id = id
        self.title = title
        self.description = description
        self.inserted_at = inserted_at
        self.publish_at = publish_at
        self.has_been_sent = has_been_sent
        self.task_message_id = task_message_id
        self.id_creator = id_creator

    def __repr__(self):
        return f"Task -> id:{self.id} title:{self.title} description:{self.description} "+\
               f"inserted_at:{self.inserted_at} publish_at:{self.publish_at} "+\
               f"has_been_sent:{self.has_been_sent} task_message_id: {self.task_message_id} "+\
               f"id_creator{self.id_creator}"


class Users_Tasks(Base):
    """ Join table between users and tasks (many to many relationship) """
    __tablename__ = 'users_tasks'
    
    user_id = Column("user_id", ForeignKey("users.id"), primary_key=True)
    task_id = Column("task_id", ForeignKey("tasks.id"), primary_key=True)
    is_completed = Column("is_completed", Boolean)

    def __init__(self, user_id, task_id, is_completed):
        self.user_id = user_id
        self.task_id = task_id
        self.is_completed = is_completed


class ServerConfigs(Base):
    """ Keeps the configuration for discord servers """
    __tablename__ = 'server_configs'

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    guild_id = Column("guild_id", Integer, unique=True)
    tasks_channel_id = Column("tasks_channel_id", Integer)
    tasks_role_id = Column("tasks_role_id", Integer)
    timezone = Column("timezone", String, default='Europe/Rome')

    def __init__(self, guild_id: int, tasks_channel_id: int, tasks_role_id: int, id: int = None, timezone: str = None):
        self.id = id
        self.guild_id = guild_id
        self.tasks_role_id = tasks_role_id
        self.tasks_channel_id = tasks_channel_id
        self.timezone = timezone

    def __repr__(self):
        return f"{self.id} {self.guild_id} {self.tasks_channel_id} {self.timezone}"


def create_all_tables():
    Base.metadata.create_all(bind=engine)
