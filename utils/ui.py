# Standard imports
import discord


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
        thread: discord.Thread = await interaction.message.create_thread(
            name="Chat", auto_archive_duration=60, reason="Chat thread."
        )
        for i in range(0, len(self.output_message), 2000):
            await thread.send(self.output_message[i : i + 2000])
        await interaction.response.edit_message(
            content="View the thread to see the full message.", view=None
        )
