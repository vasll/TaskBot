""" Handles the setup Cog """
from discord.ext import commands
import discord
from discord import Colour, Option
from discord.commands.context import ApplicationContext
from taskbot_utils import gmt_timezones
from loggers import logger
from db.database import session
import db.schemas as schemas


class Setup(commands.Cog):
    """ Cog that contains all the commands for setting up the bot """
    def __init__(self, bot):
        self.bot = bot

    @discord.command(
        name="configure", description="Configures the bot by creating roles, setting the text channel and timezones"
    )
    @commands.has_permissions(manage_roles=True)
    async def configure(
            self, ctx: ApplicationContext,
            tasks_channel: Option(discord.TextChannel, description='Text channel where tasks will be sent'),
            timezone: Option(str, description="Preferred timezone for dates/time. Default is GMT+0",
                             required=False, default='Europe/Rome', choices=gmt_timezones)
    ):
        logger.debug(f'[guild {ctx.guild.id}] [configure()]')
        await ctx.response.defer()
        embed = discord.Embed(title=":gear: Bot configuration", colour=Colour.green())

        # Get role names from server
        roles_names = [role.name for role in await ctx.guild.fetch_roles()]

        # @tasks-manager role
        try:
            if 'tasks-manager' in roles_names:
                embed.add_field(name="@tasks-manager", value=":white_check_mark: Role exists already", inline=False)
            else:
                await ctx.guild.create_role(name='tasks-manager', colour=Colour.teal())
                embed.add_field(name="@tasks-manager", value=":white_check_mark: Role created", inline=False)
        except Exception as e:
            logger.error(f"Exception while adding @tasks-manager role to guild {ctx.guild.id}: {e}")
            embed.add_field(name="@tasks-manager", value=":x: Can't create role", inline=False)
            embed.colour = Colour.red()

        # @tasks role
        try:
            if 'tasks' in roles_names:
                embed.add_field(name="@tasks", value=":white_check_mark: Role exists already", inline=False)
            else:
                await ctx.guild.create_role(name='tasks', colour=Colour.dark_teal())
                embed.add_field(name="@tasks", value=":white_check_mark: Role created", inline=False)
        except Exception as e:
            logger.error(f"Exception while adding @tasks role to guild {ctx.guild.id}: {e}")
            embed.add_field(name="@tasks", value=":x: Can't create role", inline=False)
            embed.colour = Colour.red()

        # timezone
        embed.add_field(name="timezone", value=f":white_check_mark: Timezone set as {timezone}", inline=False)

        # Add config to db
        try:
            # If GuildConfig exists update it. Otherwise create the new entry
            db_guild_config = session.query(schemas.ServerConfigs).filter_by(guild_id=ctx.guild.id).first()
            if db_guild_config is not None:
                db_guild_config.tasks_channel_id = tasks_channel.id
                db_guild_config.tasks_role_id = discord.utils.get(ctx.guild.roles, name="tasks").id
                db_guild_config.timezone = timezone
                session.commit()
            else:
                server_config = schemas.ServerConfigs(
                    guild_id = ctx.guild.id, 
                    tasks_channel_id = tasks_channel.id, 
                    tasks_role_id = discord.utils.get(ctx.guild.roles, name="tasks").id, 
                    timezone = timezone
                )
                session.add(server_config)
                session.commit()
            embed.add_field(name="Configuration", value=":white_check_mark: Configuration saved", inline=False)
        except Exception as e:
            logger.error(f"Exception while adding db.schemas.ServerConfigs entry of guild {ctx.guild.id}: {e}")
            embed.add_field(name="Configuration", value=":x: Couldn't save configuration", inline=False)
            embed.colour = Colour.red()

        await ctx.respond(embed=embed)
