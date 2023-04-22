import discord, schemas
from sqlalchemy import update
from discord.ui import Button, View
from discord import ButtonStyle, Interaction, ui
from database import session


class PersistentView(View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @ui.button(label='Completed', style=ButtonStyle.green, custom_id='task_completed')
    async def green(self, button: Button, interaction: Interaction):
        # Check first if user is in db
        db_user = session.query(schemas.Users).filter_by(id=interaction.user.id).first()
        if db_user is None:
            session.add(schemas.Users(id=interaction.user.id))
            session.commit()
            db_user = session.query(schemas.Users).filter_by(id=interaction.user.id).first()

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
            session.add(schemas.Users_Tasks(user_id=interaction.user.id, task_id=db_task.id, is_completed=True))
            session.commit()
        else:
            db_users_tasks.is_completed = True
            session.commit()
        
        await interaction.response.send_message('Marked as completed!', ephemeral=True)


    @ui.button(label='Not completed', style=ButtonStyle.red, custom_id='task_not_completed')
    async def not_completed(self, button: Button, interaction: Interaction):
        # Check first if user is in db
        db_user = session.query(schemas.Users).filter_by(id=interaction.user.id).first()
        if db_user is None:
            session.add(schemas.Users(id=interaction.user.id))
            session.commit()
            db_user = session.query(schemas.Users).filter_by(id=interaction.user.id).first()

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
        
        await interaction.response.send_message('Marked as not completed!', ephemeral=True)
