import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import asyncio
import logging
from .config.conf import DISCORD_TOKEN, COMMAND_PREFIX

load_dotenv()

logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.members = True
intents.message_content = True
intents.presences = True

bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents)
print(f"Bot ID: {id(bot)}") 

async def load_cogs():
    for folder in ["commands", "events"]:
        for filename in os.listdir(f"bot/{folder}"):
            if filename.endswith(".py") and not filename.startswith("__"):
                ext = f"bot.{folder}.{filename[:-3]}"
                try:
                    await bot.load_extension(ext)
                    logger.info(f"✅ Loaded {ext}")
                except Exception as e:
                    logger.error(f"❌ Failed to load {ext}: {e}")

async def main():
    await load_cogs()
    await bot.start(DISCORD_TOKEN)

if __name__ == "__main__":
    asyncio.run(main())