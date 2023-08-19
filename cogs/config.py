import discord
from discord.ext import commands
from discord.ext.commands import Context
from utils.config import get_config, set_config


class Config(commands.Cog):
    def __init__(self, client, generator):
        self.client = client
        self.generator = generator

    @commands.hybrid_command(
        name="clear", description="Creates a new chat history by clearing messages."
    )
    async def _clear(self, ctx: Context):
        # Clear chat history from current bot session.
        self.generator.messages = []
        # Clear chat history from messages.jsonl.
        with open("messages.jsonl", "w") as f:
            f.write("")
        await ctx.send("Cleared message's from bot's chat history.")

    # Change the bot's nickname.
    @commands.hybrid_command(name="name", description="Changes the bot's name.")
    async def _name(self, ctx: Context, name: str):
        await ctx.guild.get_member(self.client.user.id).edit(nick=name)
        await ctx.send(f"Changed my name to '{name}'.")

    # Change the bot's prefix.
    @commands.hybrid_command(name="prefix", description="Changes the bot's prefix.")
    async def _prefix(self, ctx: Context, prefix: str):
        await set_config("prefix", prefix)
        self.client.command_prefix = prefix
        await ctx.send(f"Changed my prefix to '{prefix}'.")

    # Enable/disable responding to mentions in prompts.
    @commands.hybrid_command(
        name="respond_to_mention_in_prompt",
        description="Enables/disables responding to mentions in prompts.",
    )
    async def _respond_to_mention_in_prompt(self, ctx: Context, value: bool):
        if value not in [True, False]:
            await ctx.send("Value must be True or False.")
            return
        await set_config("respond_to_mention_in_prompt", value)
        await ctx.send(
            f"{'Enabled' if value else 'Disabled'} responding to mentions in prompts."
        )

    # Help command.
    @commands.hybrid_command(name="help", description="Shows the help message.")
    async def _help(self, ctx: Context):
        prefix = await get_config("prefix")
        # Generate an embed with the help message.
        embed = discord.Embed(
            title=ctx.guild.get_member(self.client.user.id).display_name,
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
            value=f"Use the bot's command prefix (`{prefix}`) followed by a space to chat with it. For example, `{prefix} Hello!`. By default, the bot will respond to mentions in prompts (for example, `What's up @{ctx.guild.get_member(self.client.user.id).display_name}?`). To disable this, use `/respond_to_mention_in_prompt False`.",
            inline=False,
        )
        embed.set_footer(
            text="Note that the bot may generate inaccurate responses that seem factual but are not, and other false/inaccurate information. By using this bot, you acknowledge that you understand this."
        )
        await ctx.send(embed=embed)
