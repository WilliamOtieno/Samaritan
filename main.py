import discord
import time
import os
import requests
import json
import random
from replit import db
from keep_alive import keep_alive

client = discord.Client()

sad_words = ["sad", "depressed", "unhappy", "angry", "grave", "hard", "lonely", "sorry", "upset", "troubled", "demise", "disappointed", "death", "obituary", "disaster", "funeral", "gloomy", "sombre", "dismal", "rejected", "gloomy", "unhappy", "miserable", "angry"]

starter_encouragements = [
    "Cheer up! ",
    "Hang in there. ",
    "You're a great person. ",
    "Don't worry. "
]

if "responding" not in db.keys():
    db["responding"] = True


def get_quote():
    response = requests.get('https://zenquotes.io/api/random')
    json_data = json.loads(response.text)
    quote = json_data[0]['q']
    return quote

def update_encouragements(encouraging_message):
    if "encouragements" in db.keys():
        encouragements = db["encouragements"]
        encouragements.append(encouraging_message)
        db["encouragements"] = encouragements
    else:
        db["encouragements"] = [encouraging_message]

def delete_encouragement(index):
    encouragements = db["encouragements"]
    if len(encouragements) > index:
        del encouragements[index]
        db["encouragements"] = encouragements



@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

# When someone joins
@client.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.channels, name="general")
    print(f'{member} has joined the server.')
    await channel.send(f"Welcome, {member}.")

# When member leaves
@client.event
async def on_member_remove(member):
    channel = discord.utils.get(member.guild.channels, name="general")
    print(f'{member} has left the server.')
    await channel.send(f"{member} has left us.")

# Clear messages
@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount)
    time.sleep(2)
    await ctx.send(f"Cleared {amount} messages.")
    print(f"Cleared {amount} messages")

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
    
    if db["responding"]:
        options = starter_encouragements
        if "encouragements" in db.keys():
            options = options + db["encouragements"]

        if any(word in msg for word in sad_words):
            quote = get_quote()
            await message.channel.send(random.choice(options))
            time.sleep(2)
            await message.channel.send(quote)

    if msg.startswith(".new"):
        encouraging_message = msg.split(".new ", 1)[1]
        update_encouragements(encouraging_message)
        await message.channel.send("New encouragement added.")
    
    if msg.startswith(".del"):
        encouragements = []
        if "encouragements" in db.keys():
            index = int(msg.split(".del",1)[1])
            delete_encouragement(index)
            encouragements = db["encouragements"]
        await message.channel.send(encouragements)

    if msg.startswith(".list"):
        encouragements = []
        if "encouragements" in db.keys():
            encouragements = db["encouragements"]
        await message.channel.send(encouragements)
    
    if msg.startswith(".responding"):
        value = msg.split(".responding ",1)[1]
        if value.lower() == "true":
            db["responding"] = True
            await message.channel.send("Responding is on.")
        else:
            db["responding"] = False
            await message.channel.send("Responding is off.")

    
keep_alive()
client.run(os.getenv('TOKEN'))

