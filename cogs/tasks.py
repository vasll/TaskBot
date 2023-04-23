""" Handles the tasks Cog """
import db.schemas as schemas, pytz, discord
from discord.ext import commands
from discord import Option
from discord.interactions import Interaction
from discord.commands.context import ApplicationContext
from loggers import logger
from db.database import session
from datetime import datetime
from views.persistent_view import PersistentView


class Tasks(commands.Cog):
    """ Cog that contains all the commands related to tasks """

    def __init__(self, bot):
        self.bot = bot

    @discord.command(name="add_task", description="Sends a task into the tasks channel of your server")
    async def add_task(
        self, ctx: ApplicationContext, 
        description: Option(str, description="Description of task", required=True),
        title: Option(str, description="Title of task", required=False, default="Task of the day")
    ):  
        await ctx.response.defer(ephemeral=True)

        # Load config data of guild
        guild_config = session.query(schemas.ServerConfigs).filter_by(guild_id=ctx.guild_id).first()
        if guild_config is None:
            return await ctx.respond("Bot was not configured\nRun the `/configure` command first!")
        tasks_role = ctx.guild.get_role(guild_config.tasks_role_id)
        tasks_channel = ctx.guild.get_channel(guild_config.tasks_channel_id)
        tasks_timezone = pytz.timezone(guild_config.timezone)

        # Send initial message with task to the tasks channel
        task_message = None
        try:
            task_message = await tasks_channel.send(
                embed = discord.Embed(
                    title = f"**:hammer: Loading task**",  description = f" ", color = 0xc7a020
                )
            )
        except Exception as e:
            print(e)

        # Check if user is already in the db
        if session.query(schemas.Users).filter_by(id=ctx.user.id).first() is None:
            session.add(schemas.Users(ctx.user.id))
            session.commit()
        
        # Add task to database
        db_task = schemas.Tasks(
            title = title,
            description = description,
            inserted_at = datetime.now(tasks_timezone),
            publish_at = datetime.now(tasks_timezone),
            has_been_sent = True,
            task_message_id = task_message.id,
            id_creator = ctx.user.id
        )
        session.add(db_task)
        session.commit()

        # Replace original message with task content
        try:
            await task_message.edit(
                content = f"{tasks_role.mention}",
                embed = discord.Embed(
                    title=f"**{title}**", 
                    description=f"# {description}\n_By {ctx.author.mention}_", 
                    color=0x58adf2
                ),
                view=PersistentView()
            )
        except Exception as e:
            print(e)
        
        await ctx.respond(f"Task has been sent in the {tasks_channel.mention} channel!")
