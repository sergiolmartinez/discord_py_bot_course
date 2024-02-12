import settings
import discord
from discord.ext import commands
from discord import app_commands

logger = settings.logging.getLogger("bot")

# get this from a database or steam api?
# future: allow players to connect their steam library and build the list based on what users in the discord server have?
# for now, just hardcode some games
games_list = {
    "among_us": {
        "title": "Among Us",
        "url": "https://cdn.cloudflare.steamstatic.com/steam/apps/945360/header.jpg?t=1698177355",
    },
    "palworld": {
        "title": "Palworld",
        "url": "https://cdn.cloudflare.steamstatic.com/steam/apps/1623730/header.jpg?t=1705662211",
    },
    "diablo": {
        "title": "Diablo",
        "url": "https://cdn.cloudflare.steamstatic.com/steam/apps/2344520/header.jpg?t=1706806800",
    },
    "cod": {
        "title": "Call of Duty: Warzone",
        "url": "https://cdn.cloudflare.steamstatic.com/steam/apps/1962663/header.jpg?t=1707420578",
    },
    "other": {
        "title": "a game",
        "url": None,
    },
}


class ReadyOrNotView(discord.ui.View):

    joined_users = []
    declined_users = []
    tentative_users = []

    initiator: discord.User = None
    players: int = 0

    async def send(self, interaction: discord.Interaction):
        self.joined_users.append(interaction.user.display_name)
        embed = self.create_embed()
        await interaction.response.send_message(view=self, embed=embed)
        self.message = await interaction.original_response()

    def convert_user_list_to_str(self, user_list, default_str="No one"):
        if len(user_list):
            return "\n".join(user_list)
        return default_str

    def create_embed(self):
        desc = f"{self.initiator.display_name} is looking for {self.players - 1} players to play {self.game['title']}. React to join!"
        embed = discord.Embed(title="Let's play together", description=desc)
        if self.game['url']:
            embed.set_image(url=self.game['url'])

        embed.add_field(inline=True, name="✅ Joined",
                        value=self.convert_user_list_to_str(self.joined_users))
        embed.add_field(inline=True, name="❌ Declined",
                        value=self.convert_user_list_to_str(self.declined_users))
        embed.add_field(inline=True, name="🔄️ Tentative",
                        value=self.convert_user_list_to_str(self.tentative_users))
        return embed

    def check_players_full(self):
        if len(self.joined_users) >= self.players:
            return True
        return False

    def disable_all_buttons(self):
        self.join_button.disabled = True
        self.decline_button.disabled = True
        self.tentative_button.disabled = True

    async def update_message(self):
        if self.check_players_full():
            self.disable_all_buttons()
            # create voice channels, message those who accepted and want to play...

        embed = self.create_embed()
        await self.message.edit(view=self, embed=embed)

    @discord.ui.button(label="Join", style=discord.ButtonStyle.green)
    async def join_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()

        # if the user is not in the joined list, then add it
        # could be better with user objects, for now do this
        if interaction.user.display_name not in self.joined_users:
            self.joined_users.append(interaction.user.display_name)
        # remove from the declined and tentative lists if inside
        if interaction.user.display_name in self.declined_users:
            self.declined_users.remove(interaction.user.display_name)
        if interaction.user.display_name in self.tentative_users:
            self.tentative_users.remove(interaction.user.display_name)

        await self.update_message()

    @discord.ui.button(label="Decline", style=discord.ButtonStyle.red)
    async def decline_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()

        # if the user is not in the declined list, then add it
        # could be better with user objects, for now do this
        if interaction.user.display_name not in self.declined_users:
            self.declined_users.append(interaction.user.display_name)
        # remove from the joined and tentative lists if inside
        if interaction.user.display_name in self.joined_users:
            self.joined_users.remove(interaction.user.display_name)
        if interaction.user.display_name in self.tentative_users:
            self.tentative_users.remove(interaction.user.display_name)

        await self.update_message()

    @discord.ui.button(label="Tentative", style=discord.ButtonStyle.blurple)
    async def tentative_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()

        # if the user is not in the tentative list, then add it
        # could be better with user objects, for now do this
        if interaction.user.display_name not in self.tentative_users:
            self.tentative_users.append(interaction.user.display_name)
        # remove from the declined and joined lists if inside
        if interaction.user.display_name in self.declined_users:
            self.declined_users.remove(interaction.user.display_name)
        if interaction.user.display_name in self.joined_users:
            self.joined_users.remove(interaction.user.display_name)

        await self.update_message()


def run():
    intents = discord.Intents.default()
    intents.message_content = True
    # intents.members = True

    bot = commands.Bot(command_prefix=settings.PREFIX, intents=intents)

    @bot.event
    async def on_ready():
        logger.info(f"User: {bot.user} - ID: {bot.user.id}")
        print(f'{bot.user} has connected to Discord! Version {discord.__version__}')
        bot.tree.copy_global_to(guild=settings.GUILDS_ID)
        await bot.tree.sync(guild=settings.GUILDS_ID)
        # try:
        #     synced = await bot.tree.sync()
        #     print(f"Synced {len(synced)} commands.")
        # except Exception as e:
        # print(e)

    @bot.tree.command()
    @app_commands.choices(game=[
        app_commands.Choice(name="Among Us", value="among_us"),
        app_commands.Choice(name="Palworld", value="palworld"),
        app_commands.Choice(name="Diablo", value="diablo"),
        app_commands.Choice(name="Warzone", value="cod"),
        app_commands.Choice(name="Other", value="other"),
    ])
    async def play(interaction: discord.Interaction, game: app_commands.Choice[str], players: int = 4):
        view = ReadyOrNotView(timeout=None)
        view.initiator = interaction.user
        view.game = games_list[game.value]
        view.players = players
        await view.send(interaction)

    bot.run(settings.DISCORD_API_SECRET, root_logger=True)


if __name__ == "__main__":
    run()
