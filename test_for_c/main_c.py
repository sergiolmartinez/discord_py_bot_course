from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message
from test_for_c.responses import send_message

# STEP 0: LOAD OUR TOKEN FROM SOMEWHERE SAFE
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_API_TOKEN')

# STEP 1: BOT SETUP
intents: Intents = Intents.default()
intents.message_content = True
client: Client = Client(intents=intents)

# STEP 3: HANDLING THE STARTUP FOR OUR BOT


@client.event
async def on_ready() -> None:
    print(f'{client.user} is now running!')

# STEP 4: HANDLING INCOMING MESSAGES


@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user:
        return

    username: str = str(message.author)
    user_message: str = message.content
    channel: str = str(message.channel)

    if message.guild and client.user.mentioned_in(message):
        print(f'[{channel}] {username}: "{user_message}"')
        await send_message(message, user_message)

    elif not message.guild:
        print(f'Direct message from {username}: "{user_message}"')
        await send_message(message, user_message)

# STEP 5: MAIN ENTRY POINT


def main() -> None:
    client.run(token=TOKEN)


if __name__ == '__main__':
    main()
