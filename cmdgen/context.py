"""
cmdgen/context.py

Purpose:
This file gathers information about the environment where the user is running the tool.
It detects the Operating System, the shell (e.g. bash, powershell), and the current 
working directory so that the AI can generate commands tailored perfectly to their system.
"""
import os
import platform

def get_os_name() -> str:
    """Returns the name of the operating system."""
    return platform.system() + " " + platform.release()

def get_shell_name() -> str:
    """Attempts to determine the current shell running the tool."""
    # On Windows, COMSPEC is usually set to cmd.exe or powershell.exe
    # On Unix, SHELL is usually set to /bin/bash, /bin/zsh, etc.
    shell = os.environ.get("SHELL")
    if shell:
        return shell.split(os.sep)[-1]
    
    comspec = os.environ.get("COMSPEC")
    if comspec:
        return comspec.split(os.sep)[-1]
        
    return "unknown"

def get_cwd() -> str:
    """Returns the current working directory."""
    return os.getcwd()
