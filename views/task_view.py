from datetime import datetime
import pytz
from discord.ui import Button, View
from discord import ButtonStyle, Interaction, ui
from db import queries
from db.schemas import UsersTasks, User
from loggers import logger


class TaskView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @ui.button(label='Completed', style=ButtonStyle.green, custom_id='task_completed')
    async def green(self, button: Button, interaction: Interaction):
        # Create the user if it doesn't exist
        try:
            await queries.add_user(User(id=interaction.user.id))
        except Exception as e:
            logger.error(f"Exception while creating user in db: {e}")
            return await interaction.response.send_message("Error: couldn't add user to database")

        # Get task from db
        db_task = await queries.get_task(task_message_id=interaction.message.id)
        if db_task is None:
            return await interaction.response.send_message(
                "Error: Didn't find any task linked to this button", ephemeral=True
            )

        # Get users_tasks entry
        db_users_tasks = await queries.get_users_tasks(interaction.user.id, db_task.id)

        # Add or update users_tasks entry
        try:
            if db_users_tasks is None:
                await queries.add_users_tasks(UsersTasks(
                    user_id=interaction.user.id, task_id=db_task.id, is_completed=True,
                    updated_at=datetime.now(pytz.utc)
                ))
            else:
                await queries.update_users_tasks(
                    db_users_tasks, is_completed=True, updated_at=datetime.now(pytz.utc)
                )
        except Exception as e:
            logger.error(f"Exception while adding/updating users_task entry. Exception: {e}")
            return await interaction.response.send_message(
                "Error while updating entry in database", ephemeral=True
            )

        # Update the view's buttons with the new completed/not completed count
        completed_count = await queries.get_completed_count(db_task.id, True)
        button.label = f"{completed_count} Completed"

        not_completed_count = await queries.get_completed_count(db_task.id, False)
        self.get_item('task_not_completed').label = f"{not_completed_count} Not completed"

        await interaction.response.edit_message(view=self)

    @ui.button(label='Not completed', style=ButtonStyle.red, custom_id='task_not_completed')
    async def not_completed(self, button: Button, interaction: Interaction):
        # Create the user if it doesn't exist
        try:
            await queries.add_user(User(id=interaction.user.id))
        except Exception as e:
            logger.error(f"Exception while creating user in db: {e}")
            return await interaction.response.send_message("Error: couldn't add user to database")

        # Get task from db
        db_task = await queries.get_task(task_message_id=interaction.message.id)
        if db_task is None:
            return await interaction.response.send_message(
                "Error: Didn't find any task linked to this button", ephemeral=True
            )

        # Get users_tasks entry
        db_users_tasks = await queries.get_users_tasks(interaction.user.id, db_task.id)

        # Add or update users_tasks entry
        try:
            if db_users_tasks is None:
                await queries.add_users_tasks(UsersTasks(
                    user_id=interaction.user.id, task_id=db_task.id, is_completed=False,
                    updated_at=datetime.now(pytz.utc)
                ))
            else:
                await queries.update_users_tasks(
                    db_users_tasks, is_completed=False, updated_at=datetime.now(pytz.utc)
                )
        except Exception as e:
            logger.error(f"Exception while adding/updating users_task entry. Exception: {e}")
            return await interaction.response.send_message(
                "Error while updating entry in database", ephemeral=True
            )

        # Update the view's buttons with the new completed/not completed count
        not_completed_count = await queries.get_completed_count(db_task.id, False)
        button.label = f"{not_completed_count} Not completed"

        completed_count = await queries.get_completed_count(db_task.id, True)
        self.get_item('task_completed').label = f"{completed_count} Completed"

        await interaction.response.edit_message(view=self)
