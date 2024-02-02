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
        print("Bot is ready!")

    @bot.group()
    async def math(ctx):
        """ """
        if ctx.invoked_subcommand is None:
            await ctx.send(f"No, {ctx.subcommand_passed} does not belong to math")

    @math.group()
    async def simple(ctx):
        """ """
        if ctx.invoked_subcommand is None:
            await ctx.send(f"No, {ctx.subcommand_passed} does not belong to simple")

    @simple.command()
    async def add(ctx, one: int, two: int):
        """ Adds two numbers together"""
        await ctx.send(one + two)

    @simple.command()
    async def subtract(ctx, one: int, two: int):
        """ Subtracts two numbers """
        await ctx.send(one - two)

    bot.run(settings.DISCORD_API_SECRET, root_logger=True)


if __name__ == "__main__":
    run()
