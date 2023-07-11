""" Contains the Misc Cog """
import discord
from discord import ApplicationContext, Colour
from discord.ext import commands
from db import queries


class Misc(commands.Cog):
    """ Cog that contains miscellaneous commands """
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    @discord.command(name="logs", description="Shows some information about the TaskBot for this server")
    async def logs(self, ctx: ApplicationContext):
        await ctx.response.defer()

        task_count = await queries.get_task_count()
        task_count_guild = await queries.get_task_count_from_guild(ctx.guild.id)
        task_count_guild_completed = await queries.get_completed_task_count_from_guild(ctx.guild.id, True)
        task_count_guild_not_completed = await queries.get_completed_task_count_from_guild(ctx.guild.id, False)

        embed = discord.Embed(
            title="TaskBot logs",
            description=f":globe_with_meridians: Handling **{task_count} tasks** in **{len(self.bot.guilds)} servers**",
            colour=Colour.blue()
        )
        embed.add_field(name="Tasks in this server", value=task_count_guild)
        embed.add_field(name="Tasks completed by users in this server", value=task_count_guild_completed)
        embed.add_field(name="Tasks not completed by users in this server", value=task_count_guild_not_completed)

        await ctx.respond(embed=embed)
