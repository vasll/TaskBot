""" Contains the schemas for the TaskBot's sqlite database """
from sqlalchemy import ForeignKey, Integer, String, Column, Boolean
from db.database import Base


class User(Base):
    """ Keeps the id of a Discord user """
    __tablename__ = 'users'

    id = Column("id", Integer, primary_key=True, autoincrement=False)
    def __init__(self, id: int):
        self.id = id
    
    def __repr__(self):
        return f"User -> id:{self.id}"


class Guild(Base):
    """ Contains a discord guild id and other configuration fields that are needed for TaskBot """
    __tablename__ = 'guilds'

    id = Column("id", Integer, primary_key=True, autoincrement=False)
    tasks_channel_id = Column("tasks_channel_id", Integer)
    default_task_title = Column("default_task_title", String)

    def __init__(
            self, 
            tasks_channel_id: int, 
            default_task_title: str = "New task", 
            id: int = None
        ):
        self.id = id
        self.tasks_channel_id = tasks_channel_id
        self.default_task_title = default_task_title

    def __repr__(self):
        return f"{self.id} {self.tasks_channel_id} {self.default_task_title}"


class Task(Base):
    """ Represents a task """
    __tablename__ = 'tasks'

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    title = Column("title", String)
    description = Column("description", String)
    inserted_at = Column("inserted_at", String)
    publish_at = Column("publish_at", String)         # TODO field for scheduled tasks (not yet implemented)
    has_been_sent = Column("has_been_sent", Boolean)  # TODO field is for scheduled tasks (not yet implemented)
    task_message_id = Column("task_message_id", Integer, unique=True)
    id_creator = Column("id_creator", ForeignKey("users.id"))
    id_guild = Column("id_guild", ForeignKey("guilds.id"))

    def __init__(
            self, title, description, inserted_at, publish_at, has_been_sent, 
            task_message_id, id_creator, id_guild, id = None,
        ) -> None:
        self.id = id
        self.title = title
        self.description = description
        self.inserted_at = inserted_at
        self.publish_at = publish_at
        self.has_been_sent = has_been_sent
        self.task_message_id = task_message_id
        self.id_creator = id_creator
        self.id_guild = id_guild

    def __repr__(self):
        return f"Task -> id:{self.id} title:{self.title} description:{self.description} "+\
               f"inserted_at:{self.inserted_at} publish_at:{self.publish_at} "+\
               f"has_been_sent:{self.has_been_sent} task_message_id: {self.task_message_id} "+\
               f"id_creator: {self.id_creator} id_guild: {self.id_guild}"


class UsersTasks(Base):
    """ Join table between users and tasks (many to many relationship) """
    __tablename__ = 'users_tasks'
    
    user_id = Column("user_id", ForeignKey("users.id"), primary_key=True)
    task_id = Column("task_id", ForeignKey("tasks.id"), primary_key=True)
    is_completed = Column("is_completed", Boolean)
    updated_at = Column("updated_at", String)

    def __init__(self, user_id, task_id, is_completed, updated_at):
        self.user_id = user_id
        self.task_id = task_id
        self.is_completed = is_completed
        self.updated_at = updated_at
