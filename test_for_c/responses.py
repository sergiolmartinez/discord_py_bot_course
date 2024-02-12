from random import choice, randint
from discord import Message, User

def get_response(user_input: str) -> str:
    lowered: str = user_input.lower()

    if lowered == '':
        return 'Well, you\'re awfully silent...'
    elif 'hello' in lowered:
        return 'Hello there!'
    elif 'how are you' in lowered:
        return 'Good, thanks!'
    elif 'bye' in lowered:
        return 'See you!'
    elif 'roll dice' in lowered:
        return f'You rolled: {randint(1, 6)}'
    elif 'roll d20' in lowered:
        return f'You rolled: {randint(1, 20)}'
    else:
        return choice(['I do not understand...',
                       'What are you talking about?',
                       'Do you mind rephrasing that?'])

async def send_message(message: Message, user_message: str) -> None:
    try:
        response: str = get_response(user_message)

        # Check if the bot was mentioned and the user requested a direct message
        if message.mentions and message.mentions[0] == message.guild.me and 'message me' in user_message.lower():
            # Get the user to send a DM
            user: User = message.author
            await user.send("Lemme slide into your DMs!")
            return

        # Send the response to the appropriate channel
        await message.channel.send(response)

    except Exception as e:
        print(e)