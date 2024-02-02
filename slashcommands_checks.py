import enum
import typing
import settings
import discord
from discord.ext import commands
from discord import app_commands

logger = settings.logging.getLogger("bot")


def is_owner():
    def predicate(interaction: discord.Interaction):
        if interaction.user.id == interaction.guild.owner_id:
            return True
    return app_commands.check(predicate)


def run():
    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True

    bot = commands.Bot(command_prefix=settings.PREFIX, intents=intents)

    @bot.event
    async def on_ready():
        logger.info(f"User: {bot.user} - ID: {bot.user.id}")
        print(f'{bot.user} has connected to Discord! Version {discord.__version__}')
        logger.info(f"Guild ID: {bot.guilds[0].id}")
        bot.tree.copy_global_to(guild=settings.GUILDS_ID)
        try:
            synced = await bot.tree.sync(guild=settings.GUILDS_ID)
            print(f"Synced {len(synced)} commands.")
        except Exception as e:
            print(e)

    @bot.tree.command()
    @is_owner()
    async def say(interaction: discord.Interaction, text_to_send: str):
        """ Simon says... """
        await interaction.response.send_message(f"{text_to_send}", ephemeral=True)

    @say.error
    async def say_error(interaction: discord.Interaction, error):
        await interaction.response.send_message("Not allowed", ephemeral=True)

    bot.run(settings.DISCORD_API_SECRET, root_logger=True)


if __name__ == "__main__":
    run()
