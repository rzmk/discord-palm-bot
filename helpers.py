from dotenv import load_dotenv
from os import getenv
import google.generativeai as palm

# Config
load_dotenv()
PALM_API_KEY = getenv("PALM_API_KEY")
palm.configure(api_key=PALM_API_KEY)

class PalmOutputGenerator:
    def __init__(self):
        self.response = palm.chat(messages=["Hi"])

    async def generate_palm_output(self, prompt):
        self.response = self.response.reply(prompt)
        return self.response.last
