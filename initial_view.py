import settings
import discord
from discord.ext import commands

logger = settings.logging.getLogger("bot")


class SimpleVIew(discord.ui.View):

    foo: bool = None

    async def disable_all_items(self):
        for item in self.children:
            item.disabled = True
        await self.message.edit(view=self)

    async def on_timeout(self) -> None:
        await self.message.channel.send("Timeout")
        await self.disable_all_items()

    @discord.ui.button(label="Press here", style=discord.ButtonStyle.success)
    async def hello(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Hello World!")
        self.foo = True
        self.stop()

    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.red)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Cancelling")
        self.foo = False
        self.stop()


def run():
    intents = discord.Intents.default()
    intents.message_content = True

    bot = commands.Bot(command_prefix=settings.PREFIX, intents=intents)

    @bot.event
    async def on_ready():
        logger.info(f"User: {bot.user} - ID: {bot.user.id}")
        print("Bot is ready!")

    @bot.command()
    async def button(ctx):
        # view = discord.ui.View()
        view = SimpleVIew(timeout=50)
        # button = discord.ui.Button(label="Click me!")
        # view.add_item(button)
        message = await ctx.send(view=view)
        view.message = message

        await view.wait()
        await view.disable_all_items()

        if view.foo is None:
            logger.error("Timeout")

        elif view.foo is True:
            logger.error("OK")

        else:
            logger.error("Cancel")

    bot.run(settings.DISCORD_API_SECRET, root_logger=True)


if __name__ == "__main__":
    run()
