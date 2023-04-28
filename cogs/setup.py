""" Contains all the commands related to setting up the bot in a server """
import discord
from discord.ext import commands
from discord import Colour, Option, Embed, OptionChoice
from discord.commands.context import ApplicationContext
from taskbot_utils import gmt_timezones
from loggers import logger
from db.schemas import Guild
from views.role_view import RoleView
from db import queries


class Setup(commands.Cog):
    """ Cog that contains all the commands for setting up the bot """
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    @discord.command(
        name="configure",
        description="Creates or updates the bot's configuration for your server"
    )
    @commands.has_permissions(administrator=True)
    async def configure(
            self, ctx: ApplicationContext,
            tasks_channel: Option(discord.TextChannel, description='Text channel where tasks will be sent'),
            default_task_title: Option(
                str, description="The default task title for new tasks", required=False
            ),
            timezone: Option(
                str, description="Preferred timezone for dates/time. Default is 'Etc/GMT+2'",
                required=False, choices=gmt_timezones
            )
    ):
        await ctx.response.defer()
        embed = Embed(title=":gear: Bot configuration", colour=Colour.green())

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

        # Add guild to database
        try:
            # If Guild exists in db update it. Otherwise create the new entry
            db_guild = await queries.get_guild(ctx.guild.id)

            if db_guild is not None:    # Update guild
                if timezone is None:
                    timezone = db_guild.timezone
                if default_task_title is None:
                    default_task_title = db_guild.default_task_title

                await queries.update_guild(db_guild.id, tasks_channel.id, timezone, default_task_title)
            else:   # Add new guild
                await queries.add_guild(Guild(
                    id=ctx.guild.id, 
                    tasks_channel_id=tasks_channel.id, 
                    timezone=timezone,
                    default_task_title=default_task_title
                ))
            embed.add_field(name="Configuration", value=":white_check_mark: Configuration saved", inline=False)
        except Exception as e:
            logger.error(f"Exception while adding schemas.Guild to db of guild {ctx.guild.id}. Exception: {e}")
            embed.add_field(name="Configuration", value=":x: Configuration save failed", inline=False)
            embed.colour = Colour.red()
        
        await ctx.respond(embed=embed)


    @discord.command(
        name="send_role_embed", 
        description="Sends a role embed where users can self-assign the @tasks role"
    )
    @commands.has_permissions(administrator=True)
    async def send_role_embed(
        self, ctx: ApplicationContext, 
        text_channel: Option(
            discord.TextChannel, description='Text channel where role embed will be sent', required=True
        ),
        embed_title: Option(str, default=':pencil: Get the role here', required=False),
        embed_description: Option(
            str, default='Click the button below if you want to get notified when new tasks are published', 
            required=False
        ),
    ):
        await ctx.response.defer(ephemeral=True)

        try:
            await text_channel.send(
                embed=Embed(
                    title=embed_title, 
                    description=embed_description,
                    colour=Colour.blue()
                ), view=RoleView()
            )
        except Exception as e:
            logger.error(f"Error with sending embed: {e}")
            return await ctx.respond("Error: couldn't send embed")

        await ctx.respond("Embed sent!")


    # TODO cmd description
    @discord.command(name="enable_weekly_leaderboards")
    @commands.has_permissions(administrator=True)
    async def enable_weekly_leaderboards(
        self, ctx: ApplicationContext,
        day: Option(
            int, description="Day of the week when to send the leaderboard", required=True,
            choices=[
                OptionChoice("Monday", value=0), OptionChoice("Tuesday", value=1),
                OptionChoice("Wednesday", value=2), OptionChoice("Thursday", value=3),
                OptionChoice("Friday", value=4), OptionChoice("Saturday", value=5),
                OptionChoice("Sunday", value=6)
            ]
        ),
        hour: Option(
            int, description="Hour of the day when to send the leaderboard", required=True,
            min=0, max=23
        )
    ):
        await ctx.response.defer(ephemeral=True)
        # TODO everything