# Standard imports
import json
from os import path


async def get_config(key: str = None):
    # If config.json doesn't exist, create it with default values.
    if not path.exists("config.json"):
        with open("config.json", "w") as f:
            json.dump(
                {"prefix": "$", "respond_to_mention_in_prompt": True}, f, indent=4
            )

    # If a value is missing from config.json, add it with a default value.
    config = json.loads(open("config.json", "r").read())
    if "prefix" not in config:
        config["prefix"] = "$"
    if "respond_to_mention_in_prompt" not in config:
        config["respond_to_mention_in_prompt"] = True
    json.dump(config, open("config.json", "w"), indent=4)

    # Return the value of the key if it exists, otherwise return the whole config.
    if key:
        return config[key]
    else:
        return config


async def set_config(key: str, value: str):
    config = await get_config()
    config[key] = value
    with open("config.json", "w") as f:
        json.dump(config, f, indent=4)
