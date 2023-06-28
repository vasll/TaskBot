<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="">
    <img src="https://user-images.githubusercontent.com/67590845/234371223-f8d4c6ae-596b-47f7-ae88-ee23d1ee76f6.png" alt="Logo" width="82" height="82">
  </a>
  <h3 align="center">TaskBot</h3>
  <p align="center">
    A Discord bot to create tasks for your community<br>
    <a href="https://discord.com/oauth2/authorize?client_id=1096865199077732432&permissions=8&scope=bot"><strong>» Add it to your discord server</strong></a>  
  </p>
  
</div>

## Docs
_work in progress_

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
