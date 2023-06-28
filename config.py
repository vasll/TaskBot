""" Configuration file for TaskBot """

# Discord bot config
discord_bot_token = ""  # Your bot's discord token

# Google drive config
enable_backups = False  # Whether to enable google drive backups every 24h | REQUIRES A SERVICE ACCOUNT
service_account_file_path = "service_account_key.json"  # Path of the .json file containing the service account key file
backups_folder_id = ""  # ID of your google drive backups folder. Make sure that the service account can see it
