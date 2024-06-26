<!-- PROJECT LOGO -->
<br />
<div align="center">
    <a href="">
      <img src="https://user-images.githubusercontent.com/67590845/234371223-f8d4c6ae-596b-47f7-ae88-ee23d1ee76f6.png" alt="Logo" width="82" height="82">
    </a>
  <h3 align="center">TaskBot</h3>
  <p align="center">
    A Discord bot to create tasks for your community<br>
  </p>
  
</div>

# Bot usage
### `/setup create`
You can configure the bot by setting the text channel where all the tasks will be sent, for example a `#tasks` text channel

![image](https://github.com/vasll/TaskBot/assets/67590845/7e3b4237-4a05-44bd-bb85-446d44d76dfb)

### `/setup role_picker`
You can optionally send a role picker embed message in a chat where users will be able to self-assign the `@tasks` role. This role will be pinged each time a new task is published

![image](https://user-images.githubusercontent.com/67590845/234370559-1dc834a7-e62e-458f-b02f-068e1251872b.png)


### `/task add`
You can add tasks by giving them a title and description, by default tasks are sent in the tasks text channel that is set up with the /configure command

![image](https://github.com/vasll/TaskBot/assets/67590845/ca27764f-349b-438a-9f4c-56d50aac147b)

![image](https://user-images.githubusercontent.com/67590845/234368690-74535178-cdc5-48ab-934b-7cdb1d9acbea.png)


### `/task leaderboard`
Each server has its own leaderboards based on the number of completed tasks

![leaderboard](https://github.com/vasll/TaskBot/assets/67590845/084f6cec-0635-4d20-b870-7c411b7af1ac)


## Hosting
If you'd like to host this bot you can create a `config.py` file in the root directory with the structure down below. If you don't want backups of the database you can set enable_backups as False
```python
# Discord bot config
discord_bot_token: str = ""  # Your bot's discord token

# Google drive config
enable_backups: bool = False  # Whether to enable google drive backups every 24h | REQUIRES A SERVICE ACCOUNT
service_account_file_path: str = "service_account_key.json"  # Path of the .json file containing the service account key file
backups_folder_id: str = ""  # ID of your google drive backups folder. Make sure that the service account can see it
backups_frequency_hours: int = 24  # How often to perform backups.
```
