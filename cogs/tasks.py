""" Handles the tasks Cog """
from discord.ext import commands
import discord
from discord.ui import Select, View
from discord import ButtonStyle, Option, SelectOption
from discord.interactions import Interaction
from discord.commands.context import ApplicationContext
from loggers import logger
from database import session
from datetime import datetime
import schemas
import pytz
from taskbot_utils import get_motivational_quote


class Tasks(commands.Cog):
    """ Cog that contains all the commands related to tasks """

    def __init__(self, bot):
        self.bot = bot


    @discord.command(name="add_task_now", description="Publish a task now")
    async def add_task_now(
            self, ctx: ApplicationContext,
            description: Option(str, description="Description of task", required=True),
            title: Option(str, description="Title of task", required=False, default="Task of the day")
    ):
        logger.debug(f'[guild {ctx.guild.id}] [add_task()]')
        await ctx.response.defer(ephemeral=True)

        # Load config data [tasks role id, tasks text channel id]
        config = session.query(schemas.ServerConfigs).filter_by(guild_id=ctx.guild_id).first()

        if config is None:
            return await ctx.respond("Bot was not configured\nRun the `/configure` command first")

        tasks_role = ctx.guild.get_role(config.tasks_role_id)
        tasks_channel = ctx.guild.get_channel(config.tasks_channel_id)
        tasks_timezone = pytz.timezone(config.timezone)

        # Add task to database
        if session.query(schemas.Users).filter_by(id=ctx.user.id).first() is None:   # Check if the user is already in the db
            session.add(schemas.Users(ctx.user.id))
            session.commit()

        datetime_now = datetime.now(tasks_timezone)
        task_db_entry = schemas.Tasks(
            title=title,
            description=description,
            inserted_at=datetime_now,
            publish_at=datetime_now,
            has_been_sent=True,
            id_creator=ctx.user.id
        )
        session.add(task_db_entry)
        session.commit()
        

        # Create the select callback
        async def select_callback(interaction: Interaction):
            # Check if user is already in db, if not insert it
            if session.query(schemas.Users).filter_by(id=interaction.user.id).first() is None:
                session.add(schemas.Users(interaction.user.id))
                session.commit()

            select_values = select.values[0].split(';')
            marked_as = select_values[0]
            task_id = select_values[1]

            if marked_as == "completed":
                try:
                    session.add(schemas.Users_Tasks(
                        user_id=interaction.user.id,
                        task_id=task_id,
                        is_completed=True
                    ))
                    session.commit()
                    await interaction.response.send_message(f"Marked as completed!", ephemeral=True)
                except Exception as e:
                    print(e)
            elif marked_as == "not_completed":
                try:
                    session.add(schemas.Users_Tasks(
                        user_id=interaction.user.id,
                        task_id=task_id,
                        is_completed=False
                    ))
                    session.commit()
                    await interaction.response.send_message(f"Marked as not completed!", ephemeral=True)
                except Exception as e:
                    print(e)
            else:
                await interaction.response.send_message(f"Unknown interaction", ephemeral=True)

        # Create the select menu
        select = Select(
            min_values=1, max_values=1,
            options=[
                SelectOption(label="Completed", emoji="✅", value=f"completed;{task_db_entry.id}"),
                SelectOption(label="Not completed", emoji="❌", value=f"not_completed;{task_db_entry.id}")
            ]
        )
        select.callback = select_callback

        # Prepare the view
        view = View()
        view.add_item(select)

        # Prepare embed with task content
        try:
            await tasks_channel.send(
                content=f"{tasks_role.mention}",
                embed=discord.Embed(
                    title=f"**{title}**", 
                    description=f"# {description}\n_By {ctx.author.mention}_", 
                    color=0x58adf2
                ),
                view=view
            )
        except Exception as e:
            print(e)

        await ctx.respond(f"Task has been sent in the {tasks_channel.mention} channel!")
