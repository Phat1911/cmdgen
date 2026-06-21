"""
cmdgen/config.py

Purpose:
This file is responsible for managing the user's settings. It defines what the 
configuration looks like (using `pydantic`), and handles safely loading and 
saving the API keys to a local file on the user's hard drive (`~/.config/cmdgen/config.json`).
"""
import os
import json
from pathlib import Path
from pydantic import BaseModel, Field

CONFIG_DIR = Path.home() / ".config" / "cmdgen"
CONFIG_FILE = CONFIG_DIR / "config.json"

class AppConfig(BaseModel):
    provider: str = Field(default="gemini", description="The LLM provider to use")
    api_key: str = Field(default="", description="The API key for the provider")

def load_config() -> AppConfig:
    """Loads the configuration from disk, or returns default if not found."""
    if not CONFIG_FILE.exists():
        return AppConfig()
    try:
        with open(CONFIG_FILE, "r") as f:
            data = json.load(f)
            return AppConfig(**data)
    except Exception:
        # In case of corruption, return default
        return AppConfig()

def save_config(config: AppConfig) -> None:
    """Saves the configuration to disk securely."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, "w") as f:
        json.dump(config.model_dump(), f, indent=4)
    
    # Ensure strict permissions on Windows/Linux if possible
    try:
        os.chmod(CONFIG_FILE, 0o600)
    except Exception:
        pass  # Permissions might act differently on Windows
