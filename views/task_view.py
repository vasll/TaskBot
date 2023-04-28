import discord, db.schemas as schemas
from sqlalchemy import update
from discord.ui import Button, View
from discord import ButtonStyle, Interaction, ui
from db import db_utils
from db.database import session
from loggers import logger


class TaskView(View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @ui.button(label='Completed', style=ButtonStyle.green, custom_id='task_completed')
    async def green(self, button: Button, interaction: Interaction):
        # Create the user if it doesn't exist
        try:
            db_utils.create_user_if_not_exists(session, interaction.user.id)
        except Exception as e:
            logger.error(f"Exception while creating user in db: {e}")
            return await interaction.response.send_message("Error: couldn't add user to database")

        # Get task from db
        db_task = session.query(schemas.Task).filter_by(task_message_id=interaction.message.id).first()
        if db_task is None:
            return await interaction.response.send_message(
                "Error: Didn't find any task linked to this button", ephemeral=True
            )
        
        # Get users_tasks entry
        db_users_tasks = session.query(schemas.UsersTasks).filter_by(
            user_id=interaction.user.id, task_id=db_task.id
        ).first()

        # Add or update users_tasks entry
        try:
            if db_users_tasks is None:
                session.add(schemas.UsersTasks(user_id=interaction.user.id, task_id=db_task.id, is_completed=True))
                session.commit()
            else:
                db_users_tasks.is_completed = True
                session.commit()
        except Exception as e:
            logger.error(f"Exception while adding/updating users_task entry. Exception: {e}")
            return await interaction.response.send_message(
                "Error while updating users_task entry in database.",
                ephemeral=True
            )
        
        # Update the view's buttons with the new completed/not completed count
        completed_count = session.query(schemas.UsersTasks).filter_by(
            task_id = db_task.id, is_completed = True
        ).count()
        button.label = f"{completed_count} Completed"
        
        not_completed_count = session.query(schemas.UsersTasks).filter_by(
            task_id = db_task.id, is_completed = False
        ).count()
        self.get_item('task_not_completed').label = f"{not_completed_count} Not completed"
        
        await interaction.response.edit_message(view=self)


    @ui.button(label='Not completed', style=ButtonStyle.red, custom_id='task_not_completed')
    async def not_completed(self, button: Button, interaction: Interaction):
        # Create the user if it doesn't exist
        try:
            db_utils.create_user_if_not_exists(session, interaction.user.id)
        except Exception as e:
            logger.error(f"Exception while creating user in db: {e}")
            return await interaction.response.send_message("Error: couldn't add user to database")

        # Get task from db
        db_task = session.query(schemas.Task).filter_by(task_message_id=interaction.message.id).first()
        if db_task is None:
            return await interaction.response.send_message(
                "Error: Didn't find any task linked to this button", ephemeral=True
            )
        
        # Get users_tasks entry
        db_users_tasks = session.query(schemas.UsersTasks).filter_by(
            user_id=interaction.user.id, task_id=db_task.id
        ).first()

        # Add or update users_tasks entry
        try:
            if db_users_tasks is None:
                session.add(schemas.UsersTasks(user_id=interaction.user.id, task_id=db_task.id, is_completed=False))
                session.commit()
            else:
                db_users_tasks.is_completed = False
                session.commit()
        except Exception as e:
            logger.error(f"Exception while adding/updating users_task entry. Exception: {e}")
            return await interaction.response.send_message(
                "Error while updating users_task entry in database.",
                ephemeral=True
            )
        
        # Update the view's buttons with the new completed/not completed count
        not_completed_count = session.query(schemas.UsersTasks).filter_by(
            task_id = db_task.id, is_completed = False
        ).count()
        button.label = f"{not_completed_count} Not completed"
        
        completed_count = session.query(schemas.UsersTasks).filter_by(
            task_id = db_task.id, is_completed = True
        ).count()
        self.get_item('task_completed').label = f"{completed_count} Completed"
        
        await interaction.response.edit_message(view=self)