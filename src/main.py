import os
import logging
import discord
from discord import app_commands

TOKEN=os.environ['DISCORD_TOKEN']

logging.basicConfig(
    level=logging.DEBUG,  # Changed to DEBUG for more info
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger('discord_bot')

try:
    intents = discord.Intents.default()
    intents.message_content = True

    class MyBot(discord.Client):
        def __init__(self):
            super().__init__(intents=intents)
            self.tree = app_commands.CommandTree(self)

        async def setup_hook(self):
            await self.tree.sync()

    bot = MyBot()

    @bot.event
    async def on_ready():
        logger.info(f'{bot.user} has connected to Discord!')

    @bot.tree.command(name="hello")
    async def hello(interaction: discord.Interaction):
        await interaction.response.send_message(f"Gabuzo {interaction.user.name}!")

    # Add error handling around the bot.run call
    try:
        bot.run(TOKEN)
    except discord.errors.LoginFailure as e:
        logger.error(f"Login failed: {str(e)}")
        logger.debug(f"Token used: {TOKEN[:10]}...") # Only show first 10 chars for security
except Exception as e:
    logger.error(f"Startup error: {str(e)}")