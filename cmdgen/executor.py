"""
cmdgen/executor.py

Purpose:
This file handles the interactive prompt and execution of the final command.
It uses `prompt_toolkit` to allow the user to edit the generated command 
before running it, and `subprocess` to actually run the command on the OS.
"""
import subprocess
import sys
from rich.console import Console
from prompt_toolkit import PromptSession
from prompt_toolkit.lexers import PygmentsLexer
from pygments.lexers.shell import BashLexer

console = Console()

DANGEROUS_KEYWORDS = [
    "rm ", "del ", "format ", "drop ", "mkfs", "truncate"
]

def check_safety(command: str) -> None:
    """Checks if a command contains potentially dangerous keywords."""
    cmd_lower = command.lower()
    if any(keyword in cmd_lower for keyword in DANGEROUS_KEYWORDS):
        console.print("[bold yellow][WARNING] This command may be destructive! Please review carefully.[/bold yellow]")

def execute_interactive(command: str) -> None:
    """
    Presents the generated command to the user for editing and executes it.
    """
    check_safety(command)
    
    session = PromptSession()
    try:
        # Prompt the user, pre-filled with the AI's command
        final_command = session.prompt(
            "> ", 
            default=command,
            lexer=PygmentsLexer(BashLexer)
        )
        
        final_command = final_command.strip()
        if not final_command:
            console.print("[dim]Command cancelled.[/dim]")
            return

        # Execute natively
        console.print()
        subprocess.run(final_command, shell=True)
        
    except KeyboardInterrupt:
        # User pressed Ctrl+C
        console.print("\n[dim]Command cancelled by user.[/dim]")
    except EOFError:
        # User pressed Ctrl+D
        console.print("\n[dim]Command cancelled by user.[/dim]")
    except Exception as e:
        console.print(f"[bold red]Failed to execute command:[/bold red] {e}")
