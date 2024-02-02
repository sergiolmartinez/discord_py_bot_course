import random
import settings
import discord
from discord.ext import commands

logger = settings.logging.getLogger("bot")


def run():
    intents = discord.Intents.default()
    intents.message_content = True

    bot = commands.Bot(command_prefix=settings.PREFIX, intents=intents)

    @bot.event
    async def on_ready():
        logger.info(f"User: {bot.user} - ID: {bot.user.id}")

    # This is a test command for the bot simply to test the bot is working by responding with pong when pinged
    @bot.command(
        aliases=["p"],
        help="This is help",
        description="This is description",
        brief="This is brief",
        enabled=True,
    )
    async def ping(ctx):
        """ Answers with pong """
        await ctx.send("pong")

    @bot.command()
    async def say(ctx, what="nothing to say"):
        """ Says a user defined message, but only the first word"""
        await ctx.send(what)

    @bot.command()
    async def say2(ctx, *what):
        """ Simon says a user defined message """
        await ctx.send(" ".join(what))

    @bot.command()
    async def choices(ctx, *options):
        """ Chooses a random option from a list of options given by the user"""
        await ctx.send(random.choice(options))

    @bot.command()
    async def say3(ctx, what="nothing to say", why="I dont know why"):
        """ Says a user defined message, but only the first word and adds a second user defined message"""
        await ctx.send(what + why)

    @bot.command()
    async def add(ctx, one: int, two: int):
        """ Adds two numbers together"""
        await ctx.send(one + two)

    bot.run(settings.DISCORD_API_SECRET, root_logger=True)


if __name__ == "__main__":
    run()
