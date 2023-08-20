# Standard imports
from os import getenv

# Third-party imports
import discord
from discord import Message
from discord.ext import commands
from dotenv import load_dotenv

# Local imports
from utils.ai import PalmOutputGenerator
from utils.config import get_config
from utils.ui import LongMessageButtons
from cogs.config import Config

load_dotenv()

DISCORD_TOKEN = getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(
    command_prefix="$",
    intents=intents,
)
generator = PalmOutputGenerator()


@client.event
async def on_message(message: Message):
    # Ignore messages from the bot itself.
    if message.author == client.user:
        return

    prefix = await get_config("prefix")
    respond_to_mention_in_prompt = await get_config("respond_to_mention_in_prompt")
    bot_name = message.guild.get_member(client.user.id).display_name

    if (
        respond_to_mention_in_prompt and client.user.mentioned_in(message)
    ) or message.content.startswith(f"{prefix} "):
        await message.channel.typing()
        # Generate the output message and send it.
        output_message = await generator.generate_chat_output(client, message, bot_name)
        if output_message:
            if len(output_message) > 2000:
                await message.reply(
                    "The output is too long to send in one message. Choose a method for sending the output.",
                    view=LongMessageButtons(output_message),
                )
            else:
                await message.reply(output_message)
        else:
            await message.reply(
                "I'm sorry, I didn't understand that. I'm going to assume I don't remember what you just said."
            )


@client.event
async def on_ready():
    # Remove default help command.
    client.remove_command("help")
    # Add the Config cog.
    await client.add_cog(Config(client, generator))
    # Sync command tree.
    await client.tree.sync()
    # Set the prefix to the value in config.json.
    client.command_prefix = await get_config("prefix")
    print(f"We have logged in as {client.user}")


client.run(DISCORD_TOKEN)
