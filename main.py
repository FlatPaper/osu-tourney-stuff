import os

import discord, json
from RelativeRankingCalculator import RelativeRanking
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

    if str(message.content) == "!xenopaper":
        await message.channel.send("https://media.discordapp.net/attachments/731987457880490154/742601523430686781/unknown.png")

    if str(message.content) == "!namderanker":
        await message.channel.send("https://cdn.discordapp.com/attachments/724332647505199216/742762469654790194/image0.png")

    if message.author.id != 258630920024621069:
        return

    if str(message.content).startswith("!calc"):
        calculator = RelativeRanking(message)
        await calculator.run()


client.run(TOKEN)
