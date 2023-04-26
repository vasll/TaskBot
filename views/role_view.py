import discord, db.schemas as schemas
from sqlalchemy import update
from discord.ui import Button, View
from discord import ButtonStyle, Interaction, ui
from discord.utils import get
from db import db_utils
from db.database import session
from loggers import logger


class RoleView(View):
    """ View where users can self-assign their role via a button """
    def __init__(self):
        super().__init__(timeout=None)
    
    @ui.button(label='Add/Remove @tasks role', style=ButtonStyle.primary, custom_id='add_tasks_role')
    async def add_roles(self, button: Button, interaction: Interaction):
        # Create the user if it doesn't exist
        try:
            db_utils.create_user_if_not_exists(session, interaction.user.id)
        except Exception as e:
            logger.error(f"Exception while creating user in db: {e}")
            return await interaction.response.send_message("Error: couldn't add user to database")
        
        # Get serverconfig and tasks role
        db_server_config = session.query(schemas.ServerConfigs).filter_by(guild_id=interaction.guild_id).first()
        if db_server_config is None:
            return await interaction.channel.send(
                "Server configuration not found. Run the `/configure` command first."
            )
        tasks_role_id = db_server_config.tasks_role_id

        # Check if user has the role already
        if tasks_role_id in [r.id for r in interaction.user.roles]:
            await interaction.user.remove_roles(interaction.user.guild.get_role(tasks_role_id))
            return await interaction.response.send_message("Role removed!", ephemeral=True)

        # Assign role to user
        try:
            tasks_role = interaction.guild.get_role(tasks_role_id)
            await interaction.user.add_roles(tasks_role)
        except discord.errors.Forbidden as e:
            logger.error(f"Error with assigning role: {e}")
            return await interaction.response.send_message(
                "Error: Couldn't assign role because of missing permissions", ephemeral=True
            )

        await interaction.response.send_message("Role assigned!", ephemeral=True)

