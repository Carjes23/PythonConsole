"""
ui_setup.py

This module sets up the user interface for the Microcontroller Interface application.
It includes the main UI components and their configuration, including serial port
selection, command entry, data display, and plot configuration.

Functions:
    - setup_ui: Initializes and configures the UI components.
"""

import tkinter as tk
from tkinter import scrolledtext, ttk
from ui_handlers import (
    connect_button_action, 
    send_command_ui, 
    reset_data, 
    toggle_graph, 
    update_plot_config_ui, 
    send_permanent_command_ui,
    text_button_action
)
from handler_config import permanent_command_entries, read_config, plot_config
from serial_handler import find_serial_ports
import ui_context as ctx

def setup_ui(root, connect_serial, disconnect_serial):
    """
    Initializes and configures the UI components for the application.

    Args:
        root (tk.Tk): The root Tkinter window.
        connect_serial (function): Function to connect to the serial port.
        disconnect_serial (function): Function to disconnect from the serial port.

    Returns:
        tuple: The x column entry widget and y columns entry widget.
    """
    global x_coords, y_coords, lines, ax, fig, canvas

    ctx.graph_window = None
    x_coords = []
    y_coords = []
    lines = []

    permanent_command_entries.clear()

    config = read_config()
    ctx.global_config = config
    default_baudrate = config.get("baudrate", 19200)

    frame = tk.Frame(root)
    frame.pack(padx=10, pady=10)

    ports = find_serial_ports()
    ctx.port_selector = ttk.Combobox(frame, values=ports)
    if(ports):
        ctx.port_selector.set(ports[0])
    else:
        ctx.port_selector.set("No ports available")
    ctx.port_selector.pack(side=tk.LEFT, padx=5)

    baudrate_label = tk.Label(frame, text="Baud Rate:")
    baudrate_label.pack(side=tk.LEFT)

    ctx.baudrate_entry = tk.Entry(frame, width=10)
    ctx.baudrate_entry.insert(0, str(default_baudrate))
    ctx.baudrate_entry.pack(side=tk.LEFT, padx=5)

    ctx.connect_button = tk.Button(frame, text="Connect", command=lambda: connect_button_action(connect_serial, disconnect_serial))
    ctx.connect_button.pack(side=tk.LEFT, padx=5)

    command_label = tk.Label(frame, text="Enter command:")
    command_label.pack(side=tk.LEFT)

    ctx.command_entry = tk.Entry(frame, width=50)
    ctx.command_entry.pack(side=tk.LEFT, padx=5)

    send_button = tk.Button(frame, text="Send", command=send_command_ui)
    send_button.pack(side=tk.LEFT)

    reset_button = tk.Button(frame, text="Reset Data", command=reset_data)
    reset_button.pack(side=tk.LEFT, padx=5)

    data_frame = tk.Frame(root)
    data_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
    
    button_frame = tk.Frame(data_frame)
    button_frame.pack(side=tk.LEFT, padx=5)

    ctx.graph_button = tk.Button(button_frame, text="Show Graph", command=toggle_graph)
    ctx.graph_button.pack(side=tk.TOP, pady=5)
    
    ctx.text_button = tk.Button(button_frame, text="Open Text", command=text_button_action)
    ctx.text_button.pack(side=tk.TOP, pady=5)

    ctx.data_display = scrolledtext.ScrolledText(data_frame, width=80, height=20)
    ctx.data_display.pack(side=tk.LEFT, padx=5, fill=tk.BOTH, expand=True)

    ctx.data_display.tag_config('user', foreground='blue')

    permanent_frame = tk.Frame(data_frame)
    permanent_frame.pack(side=tk.RIGHT, padx=5, fill=tk.Y)

    for i in range(5):
        permanent_command_label = tk.Label(permanent_frame, text=f"Permanent {i+1}:")
        permanent_command_label.pack(anchor='w')
        permanent_command_entry = tk.Entry(permanent_frame, width=30)
        permanent_command_entry.pack(anchor='w', pady=2)
        permanent_command_entries.append(permanent_command_entry)
        permanent_send_button = tk.Button(permanent_frame, text="Send", command=lambda e=permanent_command_entry: send_permanent_command_ui(e))
        permanent_send_button.pack(anchor='w', pady=2)

        if f"permanent_command_{i+1}" in config:
            permanent_command_entry.insert(0, config[f"permanent_command_{i+1}"])

    # Add plot configuration UI
    plot_frame = tk.Frame(root)
    plot_frame.pack(padx=10, pady=10)

    x_column_label = tk.Label(plot_frame, text="X Column:")
    x_column_label.pack(side=tk.LEFT)

    ctx.x_column_entry = tk.Entry(plot_frame, width=5)
    ctx.x_column_entry.pack(side=tk.LEFT, padx=5)
    ctx.x_column_entry.insert(0, str(config.get("x_column", "")))

    y_columns_label = tk.Label(plot_frame, text="Y Columns:")
    y_columns_label.pack(side=tk.LEFT)

    ctx.y_columns_entry = tk.Entry(plot_frame, width=20)
    ctx.y_columns_entry.pack(side=tk.LEFT, padx=5)
    ctx.y_columns_entry.insert(0, ','.join(map(str, config.get("y_columns", []))))

    update_plot_button = tk.Button(plot_frame, text="Update Plot", command=update_plot_config_ui)
    update_plot_button.pack(side=tk.LEFT, padx=5)

    return ctx.x_column_entry, ctx.y_columns_entry
