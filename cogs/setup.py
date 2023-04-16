""" Handles the setup Cog """
from discord.ext import commands
import discord
from discord import Colour
from discord import Option
from discord.commands.context import ApplicationContext
from loggers import logger
from database import session
from schemas import Configs


class Setup(commands.Cog):
    """ Cog that contains all the commands for setting up the bot """

    def __init__(self, bot):
        self.bot = bot

    @discord.command(name="configure", description="Configures the bot by creating roles and binding a text channel")
    @commands.has_permissions(manage_roles=True)
    async def configure(self, ctx: ApplicationContext,
                        tasks_channel: Option(discord.TextChannel, description='Text channel where tasks will be sent')
                        ):
        logger.debug(f'[guild {ctx.guild.id}] [configure()]')
        await ctx.response.defer()
        embed = discord.Embed(title=":gear: Bot configuration", colour=Colour.green())

        # Get roles from server
        roles_names = [role.name for role in await ctx.guild.fetch_roles()]

        # @tasks-manager role
        try:
            if 'tasks-manager' in roles_names:
                embed.add_field(name="@tasks-manager", value=":white_check_mark: Role exists already", inline=False)
            else:
                await ctx.guild.create_role(name='tasks-manager', colour=Colour.teal())
                embed.add_field(name="@tasks-manager", value=":white_check_mark: Role created", inline=False)
        except Exception as _:
            embed.add_field(name="@tasks-manager", value=":x: Can't create role", inline=False)
            embed.colour = Colour.red()

        # @tasks role
        try:
            if 'tasks' in roles_names:
                embed.add_field(name="@tasks", value=":white_check_mark: Role exists already", inline=False)
            else:
                await ctx.guild.create_role(name='tasks', colour=Colour.dark_teal())
                embed.add_field(name="@tasks", value=":white_check_mark: Role created", inline=False)
        except Exception as _:
            embed.add_field(name="@tasks", value=":x: Can't create role", inline=False)
            embed.colour = Colour.red()

        # Add config to db
        try:
            config = Configs(ctx.guild.id, tasks_channel.id)
            session.add(config)
            session.commit()
            embed.add_field(name="Config", value=":white_check_mark: Configuration saved", inline=False)
        except Exception as _:
            embed.add_field(name="Config", value=":x: Couldn't save configuration", inline=False)
            embed.colour = Colour.red()

        await ctx.respond(embed=embed)
