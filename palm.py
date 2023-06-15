import requests
from pprint import pprint
import json
from dotenv import load_dotenv
from os import getenv

load_dotenv()  # take environment variables from .env.

PALM_API_KEY = getenv("PALM_API_KEY")

def generate_palm_output(prompt):

    # with open('datainput.txt', 'r') as file:
    #     prompt = file.read()
        
        url = f"https://generativelanguage.googleapis.com/v1beta2/models/text-bison-001:generateText?key={PALM_API_KEY}"
        headers = {'Content-type': 'content_type_value'}
        import json

        data = json.dumps({
            "prompt": {
                "text": prompt
            },
            "max_output_tokens": 8192
        })

        r = requests.post(url=url, headers=headers, data=data)

        output = r.json()
        # pprint(output)
        output_message = output["candidates"][0]["output"]
        # pprint(output_message)
        return output_message
