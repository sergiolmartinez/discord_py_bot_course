import enum
import typing
import settings
import discord
from discord.ext import commands
from discord import app_commands

logger = settings.logging.getLogger("bot")


class Food(enum.Enum):
    apple = 1
    banana = 2
    orange = 3


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
    @app_commands.describe(text_to_send="Simon says this...")
    @app_commands.rename(text_to_send="message")
    async def say(interaction: discord.Interaction, text_to_send: str):
        await interaction.response.send_message(f"{text_to_send}", ephemeral=True)

    @bot.tree.command()
    async def drink(interaction: discord.Interaction, choice: typing.Literal['beer', 'whiskey', 'wine']):
        await interaction.response.send_message(f"{choice}", ephemeral=True)

    @bot.tree.command()
    async def eat(interaction: discord.Interaction, choice: Food):
        await interaction.response.send_message(f"{choice}", ephemeral=True)

    @bot.tree.command()
    @app_commands.choices(choice=[
        app_commands.Choice(name="red", value="1"),
        app_commands.Choice(name="yellow", value="2"),
        app_commands.Choice(name="blue", value="3")
    ])
    async def color(interaction: discord.Interaction, choice: app_commands.Choice[str]):
        await interaction.response.send_message(f"{choice}", ephemeral=True)

    bot.run(settings.DISCORD_API_SECRET, root_logger=True)


if __name__ == "__main__":
    run()
