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
        print(f'{bot.user} has connected to Discord! Version {discord.__version__}')
        logger.info(f"Guild ID: {bot.guilds[0].id}")
        bot.tree.copy_global_to(guild=settings.GUILDS_ID)
        try:
            synced = await bot.tree.sync(guild=settings.GUILDS_ID)
            print(f"Synced {len(synced)} commands.")
        except Exception as e:
            print(e)

    @bot.tree.context_menu(name="Show join date")
    async def get_joined_date(interaction: discord.Interaction, member: discord.Member):
        await interaction.response.send_message(f"Member joined: {discord.utils.format_dt(member.joined_at)}", ephemeral=True)

    @bot.tree.context_menu(name="Report Message")
    async def report_message(interaction: discord.Interaction, member: discord.Message):
        await interaction.response.send_message(f"Message reported", ephemeral=True)

    # @bot.tree.context_menu(name="Report Message")
    # async def report_message(interaction: discord.Interaction, channel: discord.VoiceChannel):
    #     await interaction.response.send_message(f"Message reported", ephemeral=True)

    bot.run(settings.DISCORD_API_SECRET, root_logger=True)


if __name__ == "__main__":
    run()
