import json
import os
import atexit

CONTEXT_FILE = "user_context.json"
_agent_context = {}

def load_context_from_file() -> dict:
    """Loads the agent context from a local JSON file."""
    if os.path.exists(CONTEXT_FILE):
        with open(CONTEXT_FILE, "r") as file:
            return json.load(file)
    return {}

def save_context_to_file():
    """Saves the current context to a local JSON file."""
    with open(CONTEXT_FILE, "w") as file:
        json.dump(_agent_context, file, indent=2)

def setAgentContext() -> dict:
    """
    Loads and sets the initial context for the agent from a local file.
    
    Returns:
        dict: The loaded context.
    """
    global _agent_context
    _agent_context = load_context_from_file()

    # Register the save handler for app exit
    atexit.register(save_context_to_file)

    return _agent_context
