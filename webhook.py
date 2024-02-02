import asyncio
import discord
from discord import Webhook
import aiohttp


async def anything(url):
    async with aiohttp.ClientSession() as session:
        webhook = Webhook.from_url(url, session=session)
        embed = discord.Embed(title="This is from a webhook!")
        await webhook.send(embed=embed, username="Sergio Web")

if __name__ == "__main__":
    url = "https://discord.com/api/webhooks/1203097060685914122/bnYvQr5jmTNirfpOcL2oRCkfGrVyMyKSEMemTXH7WYUG1JC22iEjFL7YKmQKUAWTjT33"

    loop = asyncio.new_event_loop()
    loop.run_until_complete(anything(url))
    loop.close()
