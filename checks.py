import random
import settings
import discord
from discord.ext import commands
from cogs.greetings import Greetings

logger = settings.logging.getLogger("bot")


class NotOwner(commands.CheckFailure):
    ...


def is_owner():
    async def predicate(ctx):
        if ctx.author.id != ctx.guild.owner_id:
            raise NotOwner("You are not the owner of the server")
        return True
    return commands.check(predicate)


def run():
    intents = discord.Intents.default()
    intents.message_content = True

    bot = commands.Bot(command_prefix=settings.PREFIX, intents=intents)

    @bot.event
    async def on_ready():
        logger.info(f"User: {bot.user} - ID: {bot.user.id}")
        print("Bot is ready!")

    @bot.command()
    @is_owner()
    async def say(ctx, what='What?'):
        await ctx.send(what)

    @say.error
    async def say_error(ctx, error):
        if isinstance(error, NotOwner):
            await ctx.send("Permission Denied")

    bot.run(settings.DISCORD_API_SECRET, root_logger=True)


if __name__ == "__main__":
    run()
