""" Utility queries for TaskBot """
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.engine.cursor import CursorResult
from db.database import async_session, Base
from db.schemas import Guild, User, Task, UsersTasks
from loggers import logger

# TODO more/better comments

async def add_user(user_id: int) -> None:
    """ Adds a new user to the db if it doesn't exist already"""
    # TODO use User object instead of user_id param
    async with async_session() as session:
        result = await session.execute(select(User).filter_by(id = user_id))
        user = result.scalars().first()

        if user is None:
            session.add(User(id=user_id))
            await session.commit()

async def add_task(task: Task) -> None:
    """ Adds a task to the db """
    async with async_session() as session:
        session.add(task)
        await session.commit()

async def get_guild_leaderboard(guild_id: int) -> CursorResult:
    """ 
    Returns the leaderboard of the server based on how many tasks each user has completed.
    The first value of the tuple is the user's id, the second value is the count of completed tasks.
    """
    async with async_session() as session:
        result = await session.execute(text(
            "SELECT u.id, COUNT(ut.task_id) AS completed_tasks "\
            "FROM users u "\
            "JOIN users_tasks ut ON u.id = ut.user_id "\
            "JOIN tasks t ON ut.task_id = t.id "\
            "JOIN guilds g ON t.id_guild = g.id "\
            f"WHERE g.id = {guild_id} "\
            "GROUP BY u.id "\
            "ORDER BY completed_tasks DESC "\
        ))
        return result

async def get_guild(guild_id: int) -> Guild | None:
    async with async_session() as session:
        result = await session.execute(
            select(Guild).filter_by(id=guild_id).limit(1)
        )
        return result.scalars().first()

async def add_guild(guild_config: Guild) -> None:
    async with async_session() as session:
        session.add(guild_config)
        await session.commit()

async def update_guild(guild_id: int, tasks_channel_id, timezone, default_task_title) -> None:
    async with async_session() as session:
        db_guild = await get_guild(guild_id)
        db_guild.tasks_channel_id = tasks_channel_id
        db_guild.timezone = timezone
        db_guild.default_task_title = default_task_title
        await session.commit()

async def get_task(task_message_id: int) -> Task | None:
    async with async_session() as session:
        result = await session.execute(
            select(Task).filter_by(task_message_id=task_message_id).limit(1)
        )
        return result.scalars().first()

async def get_users_tasks(user_id: int, task_id: int) -> UsersTasks | None:
    async with async_session() as session:
        result = await session.execute(
            select(UsersTasks).filter_by(user_id=user_id, task_id=task_id).limit(1)
        )
        return result.scalars().first()

async def add_users_tasks(users_tasks: UsersTasks) -> None:
    async with async_session() as session:
        session.add(users_tasks)
        await session.commit()

async def update_users_tasks(users_tasks: UsersTasks, is_completed: bool) -> None:
    async with async_session() as session:
        # Get persistent object from db
        result = await session.execute(
            select(UsersTasks).filter_by(
                user_id=users_tasks.user_id,
                task_id=users_tasks.task_id
            ).limit(1)
        )
        db_users_tasks = result.scalars().first()
        db_users_tasks.is_completed = is_completed
        await session.commit()

async def get_guild_task_count(guild_id: int) -> int | None:
    async with async_session() as session:
        result = await session.execute(text(
            "SELECT COUNT(*)"\
            "FROM tasks "\
            "INNER JOIN users_tasks ON tasks.id = users_tasks.task_id "\
            "INNER JOIN guilds ON tasks.id_guild = guilds.id "\
            f"WHERE guilds.id = {guild_id}"\
        ))
        return result.first()[0]

async def get_task_count() -> int | None:
    """ Returns the task count of ALL the tasks stored in the db """
    async with async_session() as session:
        result = await session.execute(text(
            "SELECT COUNT(*) FROM tasks"
        ))
        return result.first()[0]


async def get_completed_count(task_id: int, is_completed: bool) -> int | None:
    async with async_session() as session:
        result = await session.execute(text(
            f"SELECT COUNT(DISTINCT user_id) FROM users_tasks WHERE task_id = {task_id} "\
            f"AND users_tasks.is_completed = {int(is_completed)}"
        ))
        return result.first()[0]

async def create_all_tables(engine: AsyncEngine) -> None:
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)