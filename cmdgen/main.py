"""
cmdgen/main.py

Purpose:
This is the primary entry point for the CLI application. It uses the `typer` library 
to define all the commands the user can run (like `cmdgen "query"` and `cmdgen config`).
It connects the user's input to the configuration, context, and AI logic.
"""
import typer
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from cmdgen.config import load_config, save_config

app = typer.Typer(help="AI-powered terminal command generator.")
config_app = typer.Typer(help="Manage configuration (e.g. API keys).")
app.add_typer(config_app, name="config")

console = Console()

@app.command()
def generate(
    query: list[str] = typer.Argument(..., help="The natural language query to translate into a command")
):
    """
    Generate and execute a terminal command from natural language.
    """
    query_str = " ".join(query)
    config = load_config()
    if not config.api_key:
        console.print(Panel(
            "[bold red]API Key Missing[/bold red]\n\n"
            "To use cmdgen, you need to set up your free Gemini API key.\n"
            "1. Get your key here: [link]https://aistudio.google.com/app/apikey[/link]\n"
            "2. Set it by running: [bold cyan]cmdgen config set --provider gemini --api-key \"YOUR_KEY\"[/bold cyan]",
            title="Setup Required", expand=False
        ))
        raise typer.Exit(code=1)

    # Check for new updates silently
    from cmdgen.update import check_for_updates
    check_for_updates()

    with console.status(f"[bold green]Asking {config.provider}...", spinner="dots"):
        from cmdgen.llm.gemini import GeminiProvider
        from cmdgen.context import get_os_name, get_shell_name, get_cwd
        
        provider = GeminiProvider() # We can make this dynamic later if we add OpenAI
        try:
            command, explanation = provider.generate_command(
                query=query_str,
                os_name=get_os_name(),
                shell_name=get_shell_name(),
                cwd=get_cwd(),
                api_key=config.api_key
            )
        except Exception as e:
            console.print(f"[bold red]Error generating command:[/bold red] {e}")
            raise typer.Exit(code=1)

    console.print(f"\n[bold blue]Explanation:[/bold blue] {explanation}")
    console.print("[dim]---[/dim]")
    
    from cmdgen.executor import execute_interactive
    execute_interactive(command)

@config_app.command("set")
def config_set(
    provider: str = typer.Option("gemini", help="The LLM provider (e.g., gemini, openai)"),
    api_key: str = typer.Option(..., help="The API key for the provider")
):
    """
    Set the configuration values.
    """
    config = load_config()
    config.provider = provider
    config.api_key = api_key
    save_config(config)
    console.print(f"[green]✔[/green] Configuration saved successfully! Provider set to [bold]{provider}[/bold].")

@config_app.command("view")
def config_view():
    """
    View the current configuration safely.
    """
    config = load_config()
    masked_key = f"{config.api_key[:4]}...{config.api_key[-4:]}" if len(config.api_key) > 8 else "***"
    
    console.print(Panel(
        f"[bold]Provider:[/bold] {config.provider}\n"
        f"[bold]API Key:[/bold] {masked_key}",
        title="Current Configuration", expand=False
    ))

def cli_main():
    import sys
    
    # Intercept version flags
    if "--version" in sys.argv or "-v" in sys.argv:
        from cmdgen.update import get_current_version
        console.print(f"cmdgen-ai-cli version: [bold cyan]{get_current_version()}[/bold cyan]")
        return
        
    # If the first argument is not a known subcommand or flag, default to "generate"
    if len(sys.argv) > 1 and sys.argv[1] not in ["config", "generate", "--help", "-h", "--version", "-v"]:
        sys.argv.insert(1, "generate")
    app()

if __name__ == "__main__":
    cli_main()
