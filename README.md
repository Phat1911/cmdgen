# cmdgen 🪄

An AI-powered CLI tool that translates your natural language into native terminal commands and lets you review them before execution. Powered by Google's Gemini API.

## Features

- **Natural Language to CLI:** Just type what you want to do.
- **Context-Aware:** Knows your OS (Windows/Linux/macOS), Shell, and Working Directory for perfect commands.
- **Interactive Execution:** Uses `prompt_toolkit` to let you tweak the AI's generated command before running it.
- **Safety First:** Warns you with bold yellow text if the command looks destructive (e.g., `rm`, `del`, `format`).
- **Auto-Updater:** Silently checks for updates so you're always running the best version.

## Installation

The recommended way to install Python CLI tools globally is using `pipx`:

```bash
pipx install cmdgen-ai-cli
```

*(Alternatively, you can `pip install cmdgen-ai-cli` in a virtual environment)*

## Upgrade

```bash
pipx upgrade cmdgen-ai-cli
```

## Quick Start

1. **Get an API Key:** Get a free Gemini API key from [Google AI Studio](https://aistudio.google.com/app/apikey).
2. **Configure your Key:**
   ```bash
   cg config set --provider gemini --api-key "YOUR_API_KEY"
   ```
3. **Use the Tool:**
   ```bash
   cg find all python files larger than 10MB in the current directory
   ```

You will see an explanation of the command, and an interactive prompt where you can edit it or just press `Enter` to run it!

## Configuration

View your current configuration (safely masked):
```bash
cg config view
```

## Contributing
1. Clone the repository
2. Install dependencies: `pip install -e .[dev]`
3. Run tests: `pytest`

## License
MIT
