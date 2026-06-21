"""
Purpose: Unit tests for configuration management (cmdgen/config.py).
Ensures that we can securely read, write, and handle default configurations.
"""
import pytest
from pathlib import Path

from cmdgen.config import AppConfig, load_config, save_config

@pytest.fixture
def temp_config_dir(tmp_path, monkeypatch):
    """
    Mock the config directory to point to a temporary path during tests,
    so we don't overwrite the user's real configuration.
    """
    mock_dir = tmp_path / "cmdgen_test_config"
    monkeypatch.setattr("cmdgen.config.CONFIG_DIR", mock_dir)
    monkeypatch.setattr("cmdgen.config.CONFIG_FILE", mock_dir / "config.json")
    return mock_dir

def test_load_default_config(temp_config_dir):
    """Test that loading a non-existent config returns the defaults."""
    config = load_config()
    assert config.provider == "gemini"
    assert config.api_key == ""

def test_save_and_load_config(temp_config_dir):
    """Test that we can save a configuration and load it back correctly."""
    config = AppConfig(provider="openai", api_key="test_api_key")
    save_config(config)
    
    # Ensure file was created
    config_file = temp_config_dir / "config.json"
    assert config_file.exists()
    
    # Load it back
    loaded_config = load_config()
    assert loaded_config.provider == "openai"
    assert loaded_config.api_key == "test_api_key"
