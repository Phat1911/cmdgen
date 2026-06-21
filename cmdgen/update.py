"""
Purpose: Checks PyPI for a newer version of cmdgen and notifies the user.
Caches the check to avoid slowing down the CLI on every run.
"""
import urllib.request
import json
import time
from rich.console import Console

from cmdgen.config import CONFIG_DIR

console = Console()

# We cache the update check in the config directory
UPDATE_CACHE_FILE = CONFIG_DIR / "update_check.json"
CACHE_TTL = 43200  # 12 hours in seconds
PACKAGE_NAME = "cmdgen-ai-cli"

# Fallback version for development
def get_current_version() -> str:
    try:
        from importlib.metadata import version, PackageNotFoundError
        return version(PACKAGE_NAME)
    except (ImportError, Exception):
        return "0.1.0"

def check_for_updates() -> None:
    """Silently checks PyPI for updates, at most once per day."""
    now = time.time()
    
    # Check cache
    if UPDATE_CACHE_FILE.exists():
        try:
            cache_data = json.loads(UPDATE_CACHE_FILE.read_text(encoding="utf-8"))
            if now - cache_data.get("last_check", 0) < CACHE_TTL:
                return # Skip check, too soon
        except Exception:
            pass # If cache is corrupted, ignore it

    try:
        # Fetch latest version from PyPI
        req = urllib.request.Request(
            f"https://pypi.org/pypi/{PACKAGE_NAME}/json",
            headers={"User-Agent": f"cmdgen/{get_current_version()}"}
        )
        with urllib.request.urlopen(req, timeout=1.5) as response:
            data = json.loads(response.read().decode("utf-8"))
            latest_version = data["info"]["version"]
            
        current = get_current_version()
        
        # Simple string comparison (this works well enough for simple semver like 0.1.0 vs 0.2.0)
        # We don't want to add a `packaging` dependency just for this.
        if latest_version and latest_version != current:
            console.print(f"[bold yellow]💡 A new version of cmdgen ({latest_version}) is available! Run `pip install --upgrade cmdgen-ai-cli` to update.[/bold yellow]")
            
        # Update cache
        UPDATE_CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
        UPDATE_CACHE_FILE.write_text(json.dumps({"last_check": now, "latest_version": latest_version}), encoding="utf-8")
        
    except Exception:
        # If offline or PyPI is down, silently fail. We don't want to bother the user.
        pass
