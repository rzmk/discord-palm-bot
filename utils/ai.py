# Standard imports
import json
from os import getenv, path

# Third-party imports
import google.generativeai as palm
from dotenv import load_dotenv

# Local imports
from .config import get_config, set_config

# Config
load_dotenv()
PALM_API_KEY = getenv("PALM_API_KEY")
palm.configure(api_key=PALM_API_KEY)


async def write_to_jsonl(author: str, content: str):
    # Add prompt to message history in messages.jsonl.
    with open("messages.jsonl", "a") as f:
        entry = {"author": author, "content": content}
        json.dump(entry, f)
        f.write("\n")


async def get_clean_prompt(client, message, name):
    # Get the message as the prompt and the user's display name as its name.
    clean_prompt = message.content
    prefix = await get_config("prefix")
    if message.content.startswith(prefix):
        clean_prompt = clean_prompt[len(prefix) :]
    if client.user.mentioned_in(message):
        clean_prompt = clean_prompt.replace(f"<@{client.user.id}>", f"@{name}")
    return clean_prompt


class PalmOutputGenerator:
    def __init__(self):
        self.messages = []
        # Create messages.jsonl if it doesn't exist.
        if not path.exists("messages.jsonl"):
            with open("messages.jsonl", "w") as f:
                f.write("")
        with open("messages.jsonl", "r") as file:
            for line in file:
                message_dict = json.loads(line)
                self.messages.append(message_dict)

    async def generate_palm_output(self, client, message, name):
        prompt = await get_clean_prompt(client, message, name)
        # Generate chat response.
        try:
            # If self.messages is greater than 20000 bytes, remove the first messages until it is less than 20000 bytes.
            while len(json.dumps(self.messages)) > 20000:
                self.messages.pop(0)
            response = await palm.chat_async(
                model="models/chat-bison-001",
                messages=self.messages + [{"author": "user", "content": prompt}],
                context=f"Be a helpful Discord bot named '{name}', and you will be referred to as '@{name}'.",
            )
            # If the last message was from the user, add an ellipsis to the message history.
            if len(self.messages) > 0 and self.messages[-1]["author"] == "user":
                self.messages.append({"author": "bot", "content": "..."})
                await write_to_jsonl("bot", "...")
            # Add prompt to message history.
            self.messages.append({"author": "user", "content": prompt})
            await write_to_jsonl("user", prompt)
            # Add response to message history.
            self.messages.append(
                {"author": "bot", "content": response.last if response.last else "..."}
            )
            await write_to_jsonl("bot", response.last if response.last else "...")
            # pprint(self.messages)
            # Return response.
            return response.last
        except Exception as e:
            # pprint(self.messages)
            print("Error generating response:")
            print(e)
            # If the last message was from the user, delete it from the message history.
            if len(self.messages) > 0 and self.messages[-1]["author"] == "user":
                self.messages.pop()
            return None