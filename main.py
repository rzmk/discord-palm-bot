# This example requires the 'message_content' intent.

import discord
from dotenv import load_dotenv
from os import getenv
from palm import generate_palm_output

load_dotenv()

DISCORD_BOT_CLIENT_TOKEN = getenv("DISCORD_BOT_CLIENT_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$ '):
        # Get the rest of the message after the '$ ' prefix as the prompt.
        prompt = message.content[2:]
        output_message = generate_palm_output(prompt)

        await message.channel.send(output_message)

client.run(DISCORD_BOT_CLIENT_TOKEN)
