import discord
import os
import requests
import json
import random

client = discord.Client()

sad_words = ["sad", "depressed", "unhappy", "angry", "grave", "hard", "lonely", "sorry", "upset", "troubled", "demise", "disappointed", "death", "obituary", "disaster", "funeral", "gloomy", "sombre", "dismal", "rejected", "gloomy", "unhappy", "miserable", "angry"]

starter_encouragements = [
    "Cheer up! ",
    "Hang in there. ",
    "You're a great person. ",
    "Don't worry. "
]


def get_quote():
    response = requests.get('https://zenquotes.io/api/random')
    json_data = json.loads(response.text)
    quote = json_data[0]['q']
    return quote


@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    msg = message.content

    if msg.startswith('.hello'):
        await message.channel.send('Hello!')

    if msg.startswith('.inspire'):
        quote = get_quote()
        await message.channel.send(quote)

    if any(word in msg for word in sad_words):
        await message.channel.send(random.choice(starter_encouragements))
    

client.run(os.getenv('TOKEN'))

