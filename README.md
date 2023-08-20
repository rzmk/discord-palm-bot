# 🌴 discord-palm-bot

A [Discord](https://discord.com) bot that integrates with [LangChain](https://www.langchain.com/) to use [Google's PaLM API](https://developers.generativeai.google/) using the [PaLM 2 model](https://ai.google/discover/palm2/) through MakerSuite to provide an ongoing chat. It utilizes artificial intelligence to generate responses and engage in conversations.

![Bot Demo](demo.png)

## ✨ Features

-   Interact with the PaLM API through a Discord bot, as if you're chatting with it!
-   Various slash commands!
-   The bot persists the conversation context in a local `messages.jsonl` file so it can continue the conversation even if you restart the bot. You can clear this with the `/clear` command.
-   Use a custom prefix for chatting with the bot (default set to `$`) (e.g. `$ Hi!`). You can change this prefix with the `/prefix` command, and you can even use the bot's mention as a prefix (e.g. `@my-cool-bot Hi!`)!
-   By default, mentioning the bot anywhere in your prompt will trigger a response. You can enable/disable this with the `/respond_to_mention_in_prompt` command and in `config.json`.
-   A configuration file [config.json](config.json) to persist settings, such as the bot's prefix and whether to allow the bot to respond to mentions in prompts.

![Commands example](commands-example.png)

For more details use the `/help` command with the Discord bot.

## 📚 Tech Stack

-   [Python](https://www.python.org/) - Programming language
-   [discord.py](https://discordpy.readthedocs.io/en/stable/) - Python library for Discord API
-   [LangChain](https://www.langchain.com/) - LLM abstraction library
-   [black](https://github.com/psf/black) - Python code formatter (using [the Visual Studio Code extension](https://marketplace.visualstudio.com/items?itemName=ms-python.black-formatter))

Other packages may be found in [`requirements.txt`](requirements.txt).

> **Note**: Sending multiple messages to the bot at the same time should still provide responses, but the chat history context may not be saved in the proper order. This may be an issue to resolve in the future. It is recommended to send one message at a time and wait for a response before sending another message.

## 🛠 Installation

1. Install [Python](https://www.python.org/downloads/) on your system.

2. Access the PaLM API which you can get by [joining the developer preview waitlist](https://developers.generativeai.google/) and receiving access through MakerSuite.

3. [Set up a Discord bot account and a Discord bot](https://discordpy.readthedocs.io/en/stable/discord.html) with the following settings:

-   Scopes
    -   applications.commands
    -   bot
-   Permissions
    -   Send Messages
    -   Read Messages/View Channels
-   Intents
    -   Message Content Intent

Though some of these settings may not be necessary, I've found that these are the ones that work for me.

Your resulting invite link should look similar to this:

```
https://discord.com/api/oauth2/authorize?client_id=<bot-client-id>&permissions=3072&scope=bot%20applications.commands
```

4. Add your PaLM API key and Discord bot token to a `.env` file, which you can simply do by replacing the values in the [`.env.example`](.env.example) file and renaming the file to `.env`.

> Remember to keep your API keys secret!

5. Install the necessary packages (preferably in [a virtual environment](https://realpython.com/python-virtual-environments-a-primer/)) with `pip install -r requirements.txt` and then run the bot with `python bot.py`.

The message history should be saved in a `messages.jsonl` file in the same directory as the bot, which is used when restarting the bot. You can clear this file and also the current message history with the `/clear` command.

> Note: Since there is a limit to how much data can be sent to the PaLM API at once, when the message history is large then the most recent messages within the limit are used.

## 🤝 Contributing

Contributions are welcome! If you have any ideas, fixes, or suggestions, please open an [issue](https://github.com/rzmk/discord-palm-bot/issues) or submit a [pull request](https://github.com/rzmk/discord-palm-bot/pulls).

Some documentation that may be useful include:

-   [discord.py docs](https://discordpy.readthedocs.io/en/stable/)

## 📝 License

This project is licensed under the [MIT License](LICENSE).

## Disclaimer

This bot and project are not affiliated with Discord, Google, LangChain, and MakerSuite.

By using this bot and/or project you acknowledge the following:

-   The bot and AI output may generate content that may be inaccurate and does not reflect the views of the bot owner.
-   The bot may generate inaccurate responses that seem factual but are not, and other false/inaccurate information.

Please use responsibly.
