""" Contains all the commands related to tasks """
import pytz
import discord
from discord.ext import commands
from discord import Colour, Option, SlashCommandGroup
from discord.utils import get
from discord.commands.context import ApplicationContext
from loggers import logger
from datetime import datetime
from views.task_view import TaskView
from db import queries
from db.schemas import Task, User

# TODO implement decorator that checks if ctx.user has the @tasks-manager role

class Tasks(commands.Cog):
    """ Cog that contains all the commands related to tasks """
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    task = SlashCommandGroup("task", "Task related commands")

    @task.command(name="add", description="Sends a task into the tasks channel of your server")
    async def add(
        self, ctx: ApplicationContext,
        description: Option(str, description="Description of task", required=True),
        title: Option(str, description="Title of task", required=False)
    ):
        await ctx.response.defer(ephemeral=True)

        # Check if user has the @tasks-manager role
        if 'tasks-manager' not in [r.name for r in ctx.user.roles]:
            return await ctx.respond("You need the @tasks-manager role in order to add tasks!")

        # Load config data of guild
        guild_config = await queries.get_guild_config(ctx.guild.id)
        if guild_config is None:
            return await ctx.respond("Bot was not configured\nRun the `/setup create` command first!")

        try:
            tasks_role = get(ctx.guild.roles, name="tasks")  # Fetch the @tasks role from the guild
            tasks_channel = ctx.guild.get_channel(guild_config.tasks_channel_id)
            default_task_title = guild_config.default_task_title
        except Exception as e:
            logger.info(f"Exception while fetching guild config of guild {ctx.guild.id}: {e}")
            return await ctx.respond("Error: couldn't find @tasks role or the #tasks channel was not configured")

        # Create the user if it doesn't exist
        try:
            await queries.add_user(User(id=ctx.user.id))
        except Exception as e:
            logger.error(f"Exception while creating user in db: {e}")
            return await ctx.respond("Error: couldn't add user to database")

        # If there was no task title given by the user, use the default task title from the db config
        if title is None:
            title = default_task_title

        # Send embed with task
        try:
            task_message = await tasks_channel.send(
                content=f"{tasks_role.mention}",
                embed=discord.Embed(
                    title=f"**{title}**", color=0x58adf2, description=f"**{description}**\n_By {ctx.author.mention}_"
                ),
                view=TaskView()
            )
        except Exception as e:
            logger.error(f"Exception while sending embed: {e}")
            return await ctx.respond("Error: couldn't create and send the task's embed")

        # Add task to database
        try:
            await queries.add_task(Task(
                title, description, datetime.now(pytz.utc),
                datetime.now(pytz.utc), True, task_message.id, ctx.user.id, ctx.guild.id
            ))
        except Exception as e:
            logger.error(f"Exception while adding task to database: {e}")
            return await ctx.respond("Error: couldn't add task to database")

        await ctx.respond(f"Task has been sent in the {tasks_channel.mention} channel!")

    @task.command(name="leaderboard", description="Shows the current leaderboard of tasks for this server")
    async def leaderboard(
        self, ctx: ApplicationContext,
        hide_message: Option(bool, description="Only you will see the leaderboard", default=True, required=False)
    ):
        await ctx.response.defer(ephemeral=hide_message)

        try:
            leaderboard_entries = await queries.get_guild_leaderboard(ctx.guild.id)
        except Exception as e:
            logger.error(f"Exception while fetching leaderboard for guild {ctx.guild.id}: {e}")

        embed = discord.Embed(title="TaskBot leaderboard for this server", colour=Colour.gold())

        leaderboard_users_count = 0
        for entry in leaderboard_entries:
            user_id = entry[0]     # Entry user id
            task_count = entry[1]  # The number of completed tasks of said user

            try:
                user = self.bot.get_user(user_id)
            except Exception as e:
                logger.info(f"No user found in leaderboard entry, skipping. Exception: {e}")
                continue

            if leaderboard_users_count == 0:
                embed.add_field(
                    name="First place", inline=False,
                    value=f":first_place: {user.mention} with {task_count} tasks completed"
                )
            elif leaderboard_users_count == 1:
                embed.add_field(
                    name="Second place", inline=False,
                    value=f":second_place: {user.mention} with {task_count} tasks completed"
                )
            elif leaderboard_users_count == 2:
                embed.add_field(
                    name="Third place", inline=False,
                    value=f":third_place: {user.mention} with {task_count} tasks completed"
                )
            elif leaderboard_users_count > 2:
                break

            leaderboard_users_count += 1

        await ctx.respond(embed=embed)

    @task.command(name="delete_latest", description="Deletes the latest task that you sent, if it exists")
    async def delete_latest(self, ctx: ApplicationContext):
        await ctx.response.defer(ephemeral=True)

        # Check if user has the @tasks-manager role
        if 'tasks-manager' not in [r.name for r in ctx.user.roles]:
            return await ctx.respond("You need the @tasks-manager role in order to delete tasks!")

        # Load config data of guild and get server's tasks_channel
        guild_config = await queries.get_guild_config(ctx.guild.id)
        if guild_config is None:
            return await ctx.respond("Bot was not configured\nRun the `/setup create` command first!")
        tasks_channel = ctx.guild.get_channel(guild_config.tasks_channel_id)

        # Scan the latest 100 messages sent in the tasks channel
        tasks_channel_messages = await tasks_channel.history(limit=100, oldest_first=False).flatten()
        for message in tasks_channel_messages:
            if message.author == self.bot.user:  # if message was sent by the bot it's most likely a task
                task = await queries.get_task(ctx.guild.id, message.id)

                # if user that created the task is the one that invoked the command
                if task is not None and task.id_creator == ctx.user.id:
                    await message.delete()  # Delete the discord message sent by the bot
                    await queries.delete_task(task)  # Delete the task linked to the message from the database

                    return await ctx.respond("Task deleted!")

        await ctx.respond("Couldn't find task")
