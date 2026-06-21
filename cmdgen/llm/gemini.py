"""
cmdgen/llm/gemini.py

Purpose:
This file contains the actual implementation for the Google Gemini AI. It takes the 
user's query and their system context, constructs the hidden system prompt (with 
safety filters), and calls the `google-genai` API to get the command back.
"""
from google import genai
from google.genai import types

from cmdgen.llm.base import LLMProvider

class GeminiProvider(LLMProvider):
    """Gemini implementation of the LLM Provider."""

    def generate_command(
        self, 
        query: str, 
        os_name: str, 
        shell_name: str, 
        cwd: str, 
        api_key: str
    ) -> tuple[str, str]:
        
        # Initialize the new SDK client
        client = genai.Client(api_key=api_key)

        # Use gemini-2.5-flash, the fast model
        model_name = 'gemini-2.5-flash'

        system_prompt = (
            "You are an expert systems administrator CLI assistant.\n"
            "Your job is to translate the user's natural language request into a valid, safe terminal command.\n\n"
            f"CONTEXT:\n"
            f"- OS: {os_name}\n"
            f"- Shell: {shell_name}\n"
            f"- Current Working Directory: {cwd}\n\n"
            "RULES:\n"
            "1. Output ONLY the raw command on the first line.\n"
            "2. Output a brief, 1-sentence explanation on the second line.\n"
            "3. Do not use markdown blocks (```) or quotes around the command.\n"
            "4. Ensure paths are compatible with the specified OS."
        )

        prompt = f"{system_prompt}\n\nUSER REQUEST: {query}\n\nCOMMAND AND EXPLANATION:"

        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.1 # Low temp for deterministic output
                )
            )
            
            text = response.text.strip()
            lines = text.split('\n', 1)
            
            command = lines[0].strip()
            explanation = lines[1].strip() if len(lines) > 1 else "No explanation provided."
            
            return command, explanation

        except Exception as e:
            raise RuntimeError(f"Gemini API Error: {str(e)}")
