import settings
import discord
from discord.ext import commands

logger = settings.logging.getLogger("bot")


class FavoriteGameSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Minecraft", value="mc"),
            discord.SelectOption(label="CS:GO", value="cs"),
            discord.SelectOption(label="Valorant", value="v"),
        ]
        super().__init__(options=options, placeholder="What do you like to play?", max_values=2)

    async def callback(self, interaction: discord.Interaction):
        await self.view.respond_to_answer2(interaction, self.values)


class SurveyView(discord.ui.View):
    answer1 = None
    answer2 = None

    @discord.ui.select(
        placeholder="What is your age?",
        options=[
            discord.SelectOption(label="1", value="1"),
            discord.SelectOption(label="2", value="2"),
            discord.SelectOption(label="3", value="3"),
        ]
    )
    async def select_age(self, interaction: discord.Interaction, select_item: discord.ui.Select):
        self.answer1 = select_item.values
        self.children[0].disabled = True
        game_select = FavoriteGameSelect()
        self.add_item(game_select)
        await interaction.message.edit(view=self)
        await interaction.response.defer()

    async def respond_to_answer2(self, interaction: discord.Interaction, choices):
        self.answer2 = choices
        self.children[1].disabled = True
        await interaction.message.edit(view=self)
        await interaction.response.defer()
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
    async def survey(ctx):
        view = SurveyView()
        await ctx.send(view=view)

        await view.wait()

        results = {
            "age": view.answer1,
            "games": view.answer2,
        }

        await ctx.send(f"{results}")
        await ctx.message.author.send("Thank you for your time!")

    bot.run(settings.DISCORD_API_SECRET, root_logger=True)


if __name__ == "__main__":
    run()
