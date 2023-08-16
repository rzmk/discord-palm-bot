import discord
from discord.ext import commands
from discord import Message
from dotenv import load_dotenv
from os import getenv
from helpers import PalmOutputGenerator, get_clean_prompt

load_dotenv()

DISCORD_TOKEN = getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix=commands.when_mentioned_or("$"), intents=intents)
generator = PalmOutputGenerator()

@client.event
async def on_message(message: Message):
    # Ignore messages from the bot itself.
    if message.author == client.user:
        return

    prompt = ""
    display_name = message.guild.get_member(client.user.id).display_name

    if client.user.mentioned_in(message):
        prompt = await get_clean_prompt(client, message, display_name)
        # Generate the output message and send it.
        output_message = await generator.generate_palm_output(prompt, display_name)
        if output_message:
            await message.channel.send(output_message)
        else:
            await message.channel.send("I'm sorry, I didn't understand that.")
    elif message.content.startswith("$ "):
        prompt = await get_clean_prompt(client, message, display_name)
        # Generate the output message and send it.
        output_message = await generator.generate_palm_output(prompt, display_name)
        if output_message:
            await message.channel.send(output_message)
        else:
            await message.channel.send("I'm sorry, I didn't understand that.")

@client.tree.command(name="clear", description="Creates a new chat history by clearing messages.")
async def _clear(ctx: discord.interactions.Interaction):
    generator.messages = []
    await ctx.response.send_message("Cleared chat history.")

@client.event
async def on_ready():
    # Sync command tree
    await client.tree.sync()
    print(f'We have logged in as {client.user}')

client.run(DISCORD_TOKEN)
