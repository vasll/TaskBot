""" Restores commands for the TaskBot"""
from loggers import logger
from discord import Bot
from cogs import tasks, setup, loops, misc
import config

# When subclassing discord.Bot() if new commands are added to a cog for some reason they don't get registered
# The temporary workaround is to create a raw Bot() and add the cogs to it and run it, then the commands get registered
logger.info("Registering bot commands...")
bot = Bot()
bot.add_cog(tasks.Tasks(bot))
bot.add_cog(setup.Setup(bot))
bot.add_cog(loops.Loops(bot))
bot.add_cog(misc.Misc(bot))

@bot.event
async def on_ready():
    print("Done. Exiting...")
    exit(0)

bot.run(config.discord_bot_token)
