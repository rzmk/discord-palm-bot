from dotenv import load_dotenv
from os import getenv
import google.generativeai as palm

# Config
load_dotenv()
PALM_API_KEY = getenv("PALM_API_KEY")
palm.configure(api_key=PALM_API_KEY)

class PalmOutputGenerator:
    def __init__(self):
        # Persist messages by using a .txt file.
        with open("messages.txt", "r") as f:
            # TODO: Implement better method to store and separate messages
            messages = f.read().splitlines()
            if len(messages) == 0:
                messages = ["Hi"]
            self.response = palm.chat(messages=messages)

    async def generate_palm_output(self, prompt):
        self.response = self.response.reply(prompt)
        with open("messages.txt", "a") as f:
            f.write(prompt + "\n")
            f.write(self.response.last + "\n")
        return self.response.last
