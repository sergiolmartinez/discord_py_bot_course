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

    async def drink_autocompletion(
        interaction: discord.Interaction,
        current: str
    ) -> typing.List[app_commands.Choice[str]]:
        data = []
        for drink_choice in ['beer', 'whiskey', 'wine', 'coffee', 'tea', 'water']:
            if current.lower() in drink_choice.lower():
                data.append(app_commands.Choice(
                    name=drink_choice, value=drink_choice))
        return data

    @bot.tree.command()
    @app_commands.autocomplete(item=drink_autocompletion)
    async def drink(interaction: discord.Interaction,
                    item: str
                    ):
        await interaction.response.send_message(f"{item}", ephemeral=True)

    bot.run(settings.DISCORD_API_SECRET, root_logger=True)


if __name__ == "__main__":
    run()
