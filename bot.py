import json
import discord
from os import path
from discord.ext import commands
from discord import Message, Thread
from dotenv import load_dotenv
from os import getenv
from helpers import PalmOutputGenerator, get_clean_prompt, get_config, set_config

load_dotenv()

DISCORD_TOKEN = getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(
    command_prefix="$",
    intents=intents,
)
generator = PalmOutputGenerator()


class LongMessageButtons(discord.ui.View):
    def __init__(self, output_message: str, *, timeout=180):
        super().__init__(timeout=timeout)
        self.output_message = output_message

    @discord.ui.button(
        label="Send individual messages", style=discord.ButtonStyle.blurple
    )
    async def blurple_button(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        for i in range(0, len(self.output_message), 2000):
            await interaction.channel.send(self.output_message[i : i + 2000])
        await interaction.response.edit_message(
            content="Sent individual messages.", view=None
        )

    @discord.ui.button(label="Send in thread", style=discord.ButtonStyle.gray)
    async def gray_button(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        thread: Thread = await interaction.message.create_thread(
            name="Chat", auto_archive_duration=60, reason="Chat thread."
        )
        for i in range(0, len(self.output_message), 2000):
            await thread.send(self.output_message[i : i + 2000])
        await interaction.response.edit_message(
            content="View the thread to see the full message.", view=None
        )


@client.event
async def on_message(message: Message):
    # Ignore messages from the bot itself.
    if message.author == client.user:
        return

    prompt = ""
    prefix = await get_config("prefix")
    respond_to_mention_in_prompt = await get_config("respond_to_mention_in_prompt")
    bot_name = message.guild.get_member(client.user.id).display_name

    if (
        respond_to_mention_in_prompt and client.user.mentioned_in(message)
    ) or message.content.startswith(f"{prefix} "):
        await message.channel.typing()
        prompt = await get_clean_prompt(client, message, bot_name)
        # Generate the output message and send it.
        output_message = await generator.generate_palm_output(prompt, bot_name)
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


@client.tree.command(
    name="clear", description="Creates a new chat history by clearing messages."
)
async def _clear(ctx: discord.interactions.Interaction):
    # Clear chat history from current bot session.
    generator.messages = []
    # Clear chat history from messages.jsonl.
    with open("messages.jsonl", "w") as f:
        f.write("")
    await ctx.response.send_message("Cleared message's from bot's chat history.")


# Change the bot's nickname.
@client.tree.command(name="name", description="Changes the bot's name.")
async def _name(ctx: discord.interactions.Interaction, name: str):
    await ctx.guild.get_member(client.user.id).edit(nick=name)
    await ctx.response.send_message(f"Changed my name to '{name}'.")


# Change the bot's prefix.
@client.tree.command(name="prefix", description="Changes the bot's prefix.")
async def _prefix(ctx: discord.interactions.Interaction, prefix: str):
    await set_config("prefix", prefix)
    client.command_prefix = prefix
    await ctx.response.send_message(f"Changed my prefix to '{prefix}'.")


# Enable/disable responding to mentions in prompts.
@client.tree.command(
    name="respond_to_mention_in_prompt",
    description="Enables/disables responding to mentions in prompts.",
)
async def _respond_to_mention_in_prompt(
    ctx: discord.interactions.Interaction, value: bool
):
    if value not in [True, False]:
        await ctx.response.send_message("Value must be True or False.")
        return
    await set_config("respond_to_mention_in_prompt", value)
    await ctx.response.send_message(
        f"{'Enabled' if value else 'Disabled'} responding to mentions in prompts."
    )


# Help command.
@client.tree.command(name="help", description="Shows the help message.")
async def _help(ctx: discord.interactions.Interaction):
    prefix = await get_config("prefix")
    # Generate an embed with the help message.
    embed = discord.Embed(
        title=ctx.guild.get_member(client.user.id).display_name,
        description="This bot's original GitHub source code is available [here](https://github.com/rzmk/discord-palm-bot).",
        color=ctx.guild.me.color,
    )
    embed.add_field(
        name="Commands",
        value="`/name <name>` - Changes the bot's name.\n`/clear` - Clears the bot's chat history, as if starting a new conversation.\n`/prefix <prefix>` - Changes the bot's prefix.\n`/respond_to_mention_in_prompt <True/False>` - Enables/disables responding to mentions in prompts.\n`/help` - Shows this help message.",
        inline=False,
    )
    embed.add_field(
        name="How to use",
        value=f"Use the bot's command prefix (`{prefix}`) followed by a space to chat with it. For example, `{prefix} Hello!`. By default, the bot will respond to mentions in prompts (for example, `What's up @{ctx.guild.get_member(client.user.id).display_name}?`). To disable this, use `/respond_to_mention_in_prompt False`.",
        inline=False,
    )
    embed.set_footer(
        text="Note that the bot may generate inaccurate responses that seem factual but are not, and other false/inaccurate information. By using this bot, you acknowledge that you understand this."
    )
    await ctx.response.send_message(embed=embed)


@client.event
async def on_ready():
    # Sync command tree
    await client.tree.sync()
    # Set the prefix to the value in config.json.
    client.command_prefix = await get_config("prefix")
    print(f"We have logged in as {client.user}")


client.run(DISCORD_TOKEN)
