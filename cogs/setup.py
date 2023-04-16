""" Handles the setup Cog """
from discord.ext import commands
import discord
from discord.commands.context import ApplicationContext
from loggers import logger


class Setup(commands.Cog):
    """ Cog that contains all the commands related to tasks """

    def __init__(self, bot):
        self.bot = bot

    @discord.command(name="create_roles", description="Sets up the required roles in the server")
    @commands.has_permissions(manage_roles=True)
    async def create_roles(self, ctx: ApplicationContext):
        logger.debug(f'guild.id={ctx.guild.id} cmd=create_roles')
        await ctx.response.defer(ephemeral=True)
        embed = discord.Embed(title=":busts_in_silhouette: Roles setup", color=0x77b255)

        # Get roles from server
        roles_names = [role.name for role in await ctx.guild.fetch_roles()]

        # @tasks-manager role
        try:
            if 'tasks-manager' in roles_names:
                embed.add_field(name="@tasks-manager", value=":stop_button: Role exists already", inline=False)
            else:
                await ctx.guild.create_role(name='tasks-manager', colour=discord.Colour(0x03fcba))
                embed.add_field(name="@tasks-manager", value=":white_check_mark: Role created", inline=False)
        except Exception as _:
            embed.add_field(name="@tasks-manager", value=":x: Can't create role", inline=False)
            embed.colour = 0xfbff00

        # @tasks role
        try:
            if 'tasks' in roles_names:
                embed.add_field(name="@tasks", value=":stop_button: Role exists already", inline=False)
            else:
                await ctx.guild.create_role(name='tasks', colour=discord.Colour(0x00c8ff))
                embed.add_field(name="@tasks", value=":white_check_mark: Role created", inline=False)
        except Exception as _:
            embed.add_field(name="@tasks", value=":x: Can't create role", inline=False)
            embed.colour = 0xfbff00

        await ctx.respond(embed=embed)