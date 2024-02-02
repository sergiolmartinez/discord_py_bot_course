import enum
import typing
import settings
import discord
from discord.ext import commands
from discord import app_commands

logger = settings.logging.getLogger("bot")


class SlapReason(typing.NamedTuple):
    reason: str


class SlapTransformer(app_commands.Transformer):
    async def transform(self, interaction: discord.Interaction, value: str) -> SlapReason:
        return SlapReason(reason=f"*** {value} ***")


def run():
    intents = discord.Intents.all()

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
    async def slap(interaction: discord.Interaction, reason: app_commands.Transform[SlapReason, SlapTransformer]):
        """ What did the 5 fingers say to the face? """
        await interaction.response.send_message(f"Ouch {reason}", ephemeral=True)

    @bot.tree.command()
    async def range(interaction: discord.Interaction, value: app_commands.Range[int, None, 10]):
        """ What did the 5 fingers say to the face? """
        await interaction.response.send_message(f"Ouch {value}", ephemeral=True)

    bot.run(settings.DISCORD_API_SECRET, root_logger=True)


if __name__ == "__main__":
    run()
