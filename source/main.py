import discord
import os

from discord.ext import commands
from json import loads
from pathlib import Path

from logger import create_logger

secret = loads(Path("config/secret.json").read_text())

class Manager(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="?",
            help_command=None,
            intents=discord.Intents.all(),
            application=983846918683770941,
            # The server name here is staying as is. Old server reference!
            activity=discord.Activity(name="Nincord", type=discord.ActivityType.watching),
            status=discord.Status.online
        )
        self.logger = create_logger("Main")

    async def setup_hook(self):
        for filename in os.listdir("./source"):
            # Load all of the modules in the modules folder.
            if filename.endswith(".py") and filename not in ["main.py", "logger.py"]:
                await self.load_extension(f"{filename[:-3]}")
                self.logger.info(f"Loaded {filename} successfully from the modules folder.")
    
        print(f'{bot.user} has connected to Discord!')  # Added message to console
        self.logger.info(f'{bot.user} has connected to Discord!')  # Added message to logger
        
#   @bot.command(name='restart')
#   @commands.is_owner() # Ensure that only the bot owner can run this command
#   async def restart(ctx):
#       await ctx.send('Restarting the bot's host machine... Please wait...')
#       os.system('shutdown -r -t 5 -c "Restarting Haikiri"') # Initiates a restart with a 5-second delay

bot = Manager() # Run the bot.
bot.run(secret["DISCORD_BOT_TOKEN"], log_handler=None)
