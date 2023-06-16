import discord
from dotenv import load_dotenv
from os import getenv
from helpers import PalmOutputGenerator

load_dotenv()

DISCORD_TOKEN = getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

generator = PalmOutputGenerator()

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    # Ignore messages from the bot itself.
    if message.author == client.user:
        return

    if message.content.startswith('$ '):
        # Get the rest of the message after the '$ ' prefix as the prompt.
        prompt = message.content[2:]
        # Generate the output message.
        output_message = await generator.generate_palm_output(prompt)
        # Send the output message.
        await message.channel.send(output_message)

client.run(DISCORD_TOKEN)
