import discord
from discord.ui import Button, View
from discord import ButtonStyle, Interaction, ui
from discord.utils import get
from db import queries
from db.schemas import User
from loggers import logger


class RoleView(View):
    """ View where users can self-assign their role via a button """
    def __init__(self):
        super().__init__(timeout=None)
    
    @ui.button(label='Add/Remove @tasks role', style=ButtonStyle.primary, custom_id='add_tasks_role')
    async def add_roles(self, button: Button, interaction: Interaction):
        # Create the user if it doesn't exist
        try:
            await queries.add_user(User(id=interaction.user.id))
        except Exception as e:
            logger.error(f"Exception while adding user to db: {e}")
            return await interaction.response.send_message("Error: couldn't add user to database", ephemeral=True)
        
        # Get guild configuration and tasks role
        db_guild = await queries.get_guild(interaction.guild.id)
        if db_guild is None:
            return await interaction.response.send_message(
                "Server configuration not found. Run the `/configure` command first.", ephemeral=True
            )

        # Get the @tasks role from the server
        try:
            tasks_role = get(interaction.guild.roles, name="tasks")  # Fetch the @tasks role from the guild
        except Exception as e:
            logger.info(f"Exception while fetching role @tasks of guild {interaction.guild.id}: {e}")
            return await interaction.response.send_message("Error: couldn't find @tasks role", ephemeral=True)


        # Check if user has the @tasks role already
        if tasks_role.id in [r.id for r in interaction.user.roles]:
            await interaction.user.remove_roles(tasks_role)
            return await interaction.response.send_message("Role removed!", ephemeral=True)

        # Assign role to user
        try:
            await interaction.user.add_roles(tasks_role)
        except discord.errors.Forbidden as e:
            logger.error(f"Error with assigning role: {e}")
            return await interaction.response.send_message(
                "Error: Couldn't assign role because of missing permissions", ephemeral=True
            )
        except Exception as e:
            logger.error(f"Unhandled exception with assigning role: {e}")
            return await interaction.response.send_message(
                "Error: Couldn't assign role because of an unknown error", ephemeral=True
            )

        await interaction.response.send_message("Role assigned!", ephemeral=True)

