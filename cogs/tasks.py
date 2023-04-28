""" Contains all the commands related to tasks """
import pytz, discord
from sqlalchemy import text
from discord.ext import commands
from discord import Colour, Option
from discord.utils import get
from discord.commands.context import ApplicationContext
from loggers import logger
from datetime import datetime
from views.task_view import TaskView
from db import queries
from db.schemas import Task


class Tasks(commands.Cog):
    """ Cog that contains all the commands related to tasks """
    def __init__(self, bot):
        self.bot = bot

    @discord.command(name="add_task", description="Sends a task into the tasks channel of your server")
    async def add_task(
        self, ctx: ApplicationContext, 
        description: Option(str, description="Description of task", required=True),
        title: Option(str, description="Title of task", required=False)
    ):  
        await ctx.response.defer(ephemeral=True)

        # Check if user has the @tasks-manager role
        if not 'tasks-manager' in [r.name for r in ctx.user.roles]:
            return await ctx.respond(f"You need the @tasks-manager role to add tasks!")

        # Load config data of guild
        db_guild = await queries.get_guild(ctx.guild.id)
        if db_guild is None:
            return await ctx.respond("Bot was not configured\nRun the `/configure` command first!")
        
        try:
            tasks_role = get(ctx.guild.roles, name="tasks")  # Fetch the @tasks role from the guild
            tasks_channel = ctx.guild.get_channel(db_guild.tasks_channel_id)
            tasks_timezone = pytz.timezone(db_guild.timezone)
            default_task_title = db_guild.default_task_title
        except Exception as e:
            logger.info(f"Exception while fetching guild config of guild {ctx.guild.id}: {e}")
            return await ctx.respond("Error: couldn't find @tasks role or the #tasks channel was not configured")
        
        # Create the user if it doesn't exist
        try:
            await queries.add_user(ctx.user.id)
        except Exception as e:
            logger.error(f"Exception while creating user in db: {e}")
            return await ctx.respond("Error: couldn't add user to database")
        
        # If there was no task title given by the user, use the default task title from the db config
        if title is None:
            title = default_task_title

        # Send embed with task
        try:
            task_message = await tasks_channel.send(
                content = f"{tasks_role.mention}", 
                embed = discord.Embed(
                    title=f"**{title}**", color=0x58adf2,
                    description=f"**{description}**\n_By {ctx.author.mention}_"
                ),
                view = TaskView()
            )
        except Exception as e:
            logger.error(f"Exception while sending embed: {e}")
            return await ctx.respond("Error: couldn't create and send the task's embed")
        
        # Add task to database
        try:
            await queries.add_task(Task(
                title, description, datetime.now(tasks_timezone), 
                datetime.now(tasks_timezone), True, task_message.id, ctx.user.id, ctx.guild.id
            ))
        except Exception as e:
            logger.error(f"Exception while adding task to database: {e}")
            return await ctx.respond("Error: couldn't add task to database")
        
        await ctx.respond(f"Task has been sent in the {tasks_channel.mention} channel!")


    @discord.command(name="leaderboard", description="Shows the current leaderboard of tasks for this server")
    async def leaderboard(self, ctx: ApplicationContext):  
        await ctx.response.defer(ephemeral=True)
        
        leaderboard_entries = await queries.get_guild_leaderboard(ctx.guild.id)
        for entry in leaderboard_entries:
            entry_user_id = entry[0]    # Entry user id
            entry_task_count = entry[1] # The number of completed tasks of said user

            # TODO