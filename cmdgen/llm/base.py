"""
cmdgen/llm/base.py

Purpose:
This file defines the `LLMProvider` abstract base class. It serves as a blueprint or 
"contract". It guarantees that no matter what AI provider we add in the future (Gemini, 
OpenAI, Claude, etc.), they will all have a `generate_command()` method with the same inputs.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any

class LLMProvider(ABC):
    """Abstract base class for all LLM providers."""

    @abstractmethod
    def generate_command(
        self, 
        query: str, 
        os_name: str, 
        shell_name: str, 
        cwd: str, 
        api_key: str
    ) -> tuple[str, str]:
        """
        Generate a terminal command based on a natural language query.
        
        Args:
            query: The user's natural language request.
            os_name: The operating system (e.g., Windows, Linux).
            shell_name: The shell being used (e.g., powershell, bash).
            cwd: The current working directory.
            api_key: The API key for the provider.
            
        Returns:
            A tuple of (generated_command, explanation).
        """
        pass
