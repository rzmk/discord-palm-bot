from dotenv import load_dotenv
from os import getenv
import google.generativeai as palm

# Config
load_dotenv()
PALM_API_KEY = getenv("PALM_API_KEY")
palm.configure(api_key=PALM_API_KEY)

async def get_clean_prompt(client, message, display_name):
    # Get the message as the prompt and the user's display name as its name.
    clean_prompt = message.content
    if message.content.startswith("$ "):
        clean_prompt = message.content[2:].strip()
    if client.user.mentioned_in(message):
        clean_prompt = message.content.replace(f"<@{client.user.id}>", display_name)
    return clean_prompt

class PalmOutputGenerator:
    def __init__(self):
        self.messages = []

    async def generate_palm_output(self, prompt, display_name):
        print(f"Prompt: {prompt}")
        # If the last message was from the user, add an ellipsis to the message history.
        if len(self.messages) > 0 and self.messages[-1]["author"] == "user":
            self.messages.append({
                "author": "bot",
                "content": "..."
            })
        # Add prompt to message history.
        self.messages.append({
            "author": "user",
            "content": prompt
        })
        print("Messages:")
        print(self.messages)
        # Generate chat response.
        response = palm.chat(messages=self.messages, context=f"Be a helpful Discord bot named '{display_name}'.")
        # Add response to message history.
        self.messages.append({
            "author": "bot",
            "content": response.last if response.last else "..."
        })
        # Return response.
        return response.last
