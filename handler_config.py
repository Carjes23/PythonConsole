# handler_config.py
import json
import os

CONFIG_FILE = "configTerminalIF.txt"

# Shared variables
permanent_command_entries = []
plot_config = {
    "x_column": None,
    "y_columns": []
}

def read_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as file:
            config = json.load(file)
            plot_config["x_column"] = config.get("x_column")
            plot_config["y_columns"] = config.get("y_columns", [])
            return config
    return {}

def write_config(config):
    with open(CONFIG_FILE, 'w') as file:
        json.dump(config, file)
