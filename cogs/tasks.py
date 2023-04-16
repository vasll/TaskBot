""" Handles the tasks Cog """
from discord.ext import commands
import discord
from discord import Option
from discord.commands.context import ApplicationContext
from loggers import logger
from database import session
import schemas
from datetime import datetime


class Tasks(commands.Cog):
    """ Cog that contains all the commands related to tasks """

    def __init__(self, bot):
        self.bot = bot

    @discord.command(name="add_task", description="Adds a task to TaskBot")
    async def add_task(
            self, ctx: ApplicationContext,
            content: Option(str, description="Textual content of the task", required=True),
            post_at: Option(str, description="Examples: '16/04/2023 7:30', '13/08/2024 16:30'", required=False)
    ):
        logger.debug(f'[guild {ctx.guild.id}] [add_task()]')
        await ctx.response.defer(ephemeral=True)

        discord_user_id = ctx.user.id
        insertion_date = datetime.now().strftime('%d/%m/%Y %H:%M')

        if post_at is None:
            # TODO Create the task, add it to db and post it now
            # TODO add try except
            post_at = datetime.now().strftime('%d/%m/%Y %H:%M')
            task = schemas.Tasks(ctx.user.id, insertion_date, post_at, content, has_been_sent=True)
            session.add(task)
            session.commit()
