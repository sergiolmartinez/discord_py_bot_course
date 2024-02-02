import settings
import discord
from discord.ext import commands

logger = settings.logging.getLogger("bot")


class FeedbackModal(discord.ui.Modal, title="Send us your feedback"):
    fb_title = discord.ui.TextInput(
        style=discord.TextStyle.short,
        label="Title",
        required=False,
        placeholder="Give your feedback a title"
    )

    message = discord.ui.TextInput(
        style=discord.TextStyle.long,
        label="Message",
        required=False,
        max_length=500,
        placeholder="Give your message"
    )

    async def on_submit(self, interaction: discord.Interaction):
        """This is my summary

        Args:
            interaction (discord.Interaction): Default discordpy Interaction
        """
        channel = interaction.guild.get_channel(settings.FEEDBACK_CH)

        embed = discord.Embed(title="New Feedback",
                              description=self.message.value,
                              color=discord.Color.yellow())
        embed.set_author(name=self.user.nick)

        await channel.send(embed=embed)
        await interaction.response.send_message(f"Thank you, {self.user.nick}", ephemeral=True)

    async def on_error(self, interaction: discord.Interaction, error: Exception):
        traceback.print_tb(error.__traceback__)


def run():
    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True

    bot = commands.Bot(command_prefix=settings.PREFIX, intents=intents)

    @bot.event
    async def on_ready():
        logger.info(f"User: {bot.user} - ID: {bot.user.id}")

        bot.tree.copy_global_to(guild=settings.GUILDS_ID)

        try:
            synced = await bot.tree.sync(guild=settings.GUILDS_ID)
            print(f"Synced {len(synced)} commands.")
        except Exception as e:
            print(e)

    @bot.tree.command()
    async def feedback(interaction: discord.Interaction):
        feedback_modal = FeedbackModal()
        feedback_modal.user = interaction.user
        await interaction.response.send_modal(feedback_modal)

    bot.run(settings.DISCORD_API_SECRET, root_logger=True)


if __name__ == "__main__":
    run()
