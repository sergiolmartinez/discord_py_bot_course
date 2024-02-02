import random
import settings
import discord
from discord.ext import commands
from cogs.greetings import Greetings

logger = settings.logging.getLogger("bot")


def run():
    intents = discord.Intents.default()
    intents.message_content = True

    bot = commands.Bot(command_prefix=settings.PREFIX, intents=intents)

    @bot.event
    async def on_ready():
        logger.info(f"User: {bot.user} - ID: {bot.user.id}")
        print("Bot is ready!")

        await bot.load_extension("cogs.greetings")

    bot.run(settings.DISCORD_API_SECRET, root_logger=True)


if __name__ == "__main__":
    run()
