"""Read and write application settings persisted in a local .env file."""

import os

from dotenv import dotenv_values, load_dotenv, set_key

ENV_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")

CONFIG_KEYS = [
    "JIRA_URL",
    "JIRA_EMAIL",
    "JIRA_API_TOKEN",
    "OLLAMA_URL",
    "OLLAMA_TOKEN",
    "GROQ_API_TOKEN",
    "LLM_PROVIDER",
]

DEFAULTS = {
    "OLLAMA_URL": "http://localhost:11434",
    "LLM_PROVIDER": "Auto",
}


def load_config() -> dict:
    """Return the current settings as a dict, applying defaults for missing keys."""
    load_dotenv(ENV_PATH)
    values = dotenv_values(ENV_PATH)
    config = {}
    for key in CONFIG_KEYS:
        value = values.get(key)
        if value is None or value == "":
            value = os.environ.get(key, "")
        config[key] = value if value else DEFAULTS.get(key, "")
    return config


def save_config(updates: dict) -> dict:
    """Persist the given key/value pairs to .env and return the updated config."""
    for key, value in updates.items():
        if key not in CONFIG_KEYS:
            continue
        set_key(ENV_PATH, key, str(value or ""))
    return load_config()
