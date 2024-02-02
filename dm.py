import random
import settings
import discord
from discord.ext import commands

logger = settings.logging.getLogger("bot")


def run():
    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True

    bot = commands.Bot(command_prefix=settings.PREFIX, intents=intents)

    @bot.event
    async def on_ready():
        logger.info(f"User: {bot.user} - ID: {bot.user.id}")
        print("Bot is ready!")

    @bot.command()
    async def ping(ctx):
        """ Answers with pong """
        # await ctx.message.author.send("hello")
        user = discord.utils.get(bot.guilds[0].members, nick="Serge 2")
        if user:
            await user.send("hello")

    bot.run(settings.DISCORD_API_SECRET, root_logger=True)


if __name__ == "__main__":
    run()
