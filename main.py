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

    if str(message.content) == "!mei HD1":
        await message.channel.send("Imagine getting 7x misses on HD1 Yorushika.")
        await message.channel.send("https://cdn.discordapp.com/attachments/708699255371464787/742891780923457586/speed.PNG")

    if str(message.content) == "!marvin":
        await message.channel.send("https://cdn.discordapp.com/attachments/729064000691896342/738816561346904184/unknown.png")

    if str(message.content) == "!nekopaper":
        await message.channel.send("https://cdn.discordapp.com/attachments/708699255132651608/742961583642378310/unknown.png")

    if str(message.content) == "!evan":
        await message.channel.send("https://cdn.discordapp.com/attachments/708699255132651608/744320720569630838/unknown.png")

    if message.author.id != 258630920024621069:
        return
    elif str(message.content).startswith("!calc"):
        calculator = IndividualRelativeRanking(message)
        await calculator.run()

    elif str(message.content).startswith("!track"):
        with open ('track_users.txt', 'w') as f:
            message = str(message.content)[len("!track"):]
            message = message.strip().split(",")
            for i in range(len(message)):
                f.write(message[i] + "\n")

client.run(TOKEN)
