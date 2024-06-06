"""
handler_config.py

This module handles the configuration for the Microcontroller Interface application.
It includes functions for reading from and writing to a configuration file, and
maintains shared variables for plot configuration and permanent command entries.

Functions:
    - get_executable_path: Determines the path of the executable or script.
    - read_config: Reads the configuration from a file.
    - write_config: Writes the configuration to a file.
"""

import json
import os
import sys

def get_executable_path():
    """
    Determines the path of the executable if the script is bundled by PyInstaller,
    otherwise returns the directory of the script.

    Returns:
        str: The path of the executable or script.
    """
    if getattr(sys, 'frozen', False):  # Check if running as a PyInstaller bundle
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.abspath(__file__))

# Determine the path of the executable or script
EXECUTABLE_PATH = get_executable_path()
# Define the path for the configuration file
CONFIG_FILE = os.path.join(EXECUTABLE_PATH, "configTerminalIF.txt")

# Shared variables
permanent_command_entries = []  # List to store command entries
plot_config = {
    "x_column": None,
    "y_columns": []
}

def read_config():
    """
    Reads the configuration from the configuration file.

    Returns:
        dict: The configuration as a dictionary. Returns an empty dictionary if the file does not exist.
    """
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as file:
            config = json.load(file)
            plot_config["x_column"] = config.get("x_column")
            plot_config["y_columns"] = config.get("y_columns", [])
            return config
    return {}

def write_config(config):
    """
    Writes the configuration to the configuration file.

    Args:
        config (dict): The configuration to write to the file.
    """
    with open(CONFIG_FILE, 'w') as file:
        json.dump(config, file)
