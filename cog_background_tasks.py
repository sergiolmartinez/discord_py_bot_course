import discord
from discord.ext import commands
import settings

logger = settings.logging.getLogger("bot")


def run():
    intents = discord.Intents.all()

    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.event
    async def on_ready():

        await bot.load_extension("cogs.background_tasks")

    bot.run(settings.DISCORD_API_SECRET, root_logger=True)


if __name__ == "__main__":
    run()
