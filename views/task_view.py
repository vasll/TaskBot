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

        # Get task from db
        db_task = session.query(schemas.Tasks).filter_by(task_message_id=interaction.message.id).first()
        if db_task is None:
            return await interaction.response.send_message('Error: Task not found', ephemeral=True)
        
        # Check for users_tasks entry
        db_users_tasks = session.query(schemas.Users_Tasks).filter_by(
            user_id=interaction.user.id, task_id=db_task.id
        ).first()
        # Add or update users_tasks entry
        if db_users_tasks is None:
            session.add(schemas.Users_Tasks(user_id=interaction.user.id, task_id=db_task.id, is_completed=True))
            session.commit()
        else:
            db_users_tasks.is_completed = True
            session.commit()
        
        completed_count = session.query(schemas.Users_Tasks).filter_by(
            task_id = db_task.id,
            is_completed = True
        ).count()
        button.label = f"{completed_count} Completed"
        
        not_completed_count = session.query(schemas.Users_Tasks).filter_by(
            task_id = db_task.id,
            is_completed = False
        ).count()
        self.get_item('task_not_completed').label = f"{not_completed_count} Not completed"
        
        await interaction.response.edit_message(view=self)


    @ui.button(label='Not completed', style=ButtonStyle.red, custom_id='task_not_completed')
    async def not_completed(self, button: Button, interaction: Interaction):
        # Create the user if it doesn't exist
        db_utils.create_user_if_not_exists(session, interaction.user.id)

        # Get task from db
        db_task = session.query(schemas.Tasks).filter_by(
            task_message_id=interaction.message.id
        ).first()
        if db_task is None:
            return await interaction.response.send_message('Error: Task not found', ephemeral=True)
        
        # Check for users_tasks entry
        db_users_tasks = session.query(schemas.Users_Tasks).filter_by(
            user_id=interaction.user.id, task_id=db_task.id
        ).first()
        # Add or update users_tasks entry
        if db_users_tasks is None:
            session.add(schemas.Users_Tasks(user_id=interaction.user.id, task_id=db_task.id, is_completed=False))
            session.commit()
        else:
            db_users_tasks.is_completed = False
            session.commit()
        
        not_completed_count = session.query(schemas.Users_Tasks).filter_by(
            task_id = db_task.id,
            is_completed = False
        ).count()
        button.label = f"{not_completed_count} Not completed"
        
        completed_count = session.query(schemas.Users_Tasks).filter_by(
            task_id = db_task.id,
            is_completed = True
        ).count()
        self.get_item('task_completed').label = f"{completed_count} Completed"
        await interaction.response.edit_message(view=self)