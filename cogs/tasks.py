""" Handles the tasks Cog """
from discord.ext import commands
import discord
from discord import Option
from discord.commands.context import ApplicationContext
from loggers import logger
from database import session
import schemas
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
        text_channel = ctx.guild.get_channel(config.tasks_channel_id)

        # Prepare embed task
        motivational_quote = get_motivational_quote()
        embed = discord.Embed(
            title=f"**{title}**", 
            description=f"# {description}\n_By {ctx.author.mention}_", 
            color=0x58adf2
        ).set_footer(
            text=f"{motivational_quote['content']} - {motivational_quote['author']}"
        )
        await text_channel.send(
            content=f"{tasks_role.mention}",
            embed=embed
        )
        await ctx.respond(f"Task has been sent in the {text_channel.mention} channel!")
