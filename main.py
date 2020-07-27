import os

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

client = discord.Client()


# Bot commands

@client.event
async def on_ready():
    for guild in client.guilds:
        print(f'{client.user} is connected to the following guild:\n'
              f'{guild.name}(id: {guild.id})')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

client.run(TOKEN)
