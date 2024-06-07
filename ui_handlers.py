"""
This module handles the user interface actions for the Microcontroller Interface application.
It includes functions to manage serial connection, send commands, display data, handle graph
toggle, and update plot configuration.

Functions:
    - connect_button_action: Handles connect/disconnect button action.
    - send_command_ui: Sends a command from the command entry.
    - send_permanent_command_ui: Sends a command from a permanent command entry.
    - display_user_command: Displays a user's command in the data display.
    - display_data: Displays incoming data in the data display.
    - reset_data: Resets the data and clears the data display.
    - toggle_graph: Toggles the visibility of the graph window.
    - update_plot_config_ui: Updates the plot configuration based on UI inputs.
    - update_plot: Updates the plot with new data from the data queue.
"""

from handler_config import plot_config, permanent_command_entries
from plot_handler import (
    create_plot_window, 
    close_plot_window, 
    update_graph, 
    update_plot_config, 
    recreate_plot_window, 
    parse_data
)
from serial_handler import send_command, data_queue
import tkinter as tk
import ui_context as ctx

def connect_button_action(connect_serial, disconnect_serial):
    """
    Handles the connect/disconnect button action. Connects to or disconnects from the serial port
    based on the current state of the button.

    Args:
        connect_serial (function): Function to connect to the serial port.
        disconnect_serial (function): Function to disconnect from the serial port.
    """
    if ctx.connect_button.config('text')[-1] == 'Connect':
        selected_port = ctx.port_selector.get()
        selected_baudrate = int(ctx.baudrate_entry.get())
        if selected_port:
            if connect_serial(selected_port, selected_baudrate):
                ctx.port_selector.config(state='disabled')
                ctx.baudrate_entry.config(state='disabled')
                ctx.connect_button.config(text='Disconnect')
    else:
        disconnect_serial()
        ctx.port_selector.config(state='normal')
        ctx.baudrate_entry.config(state='normal')
        ctx.connect_button.config(text='Connect')

def send_command_ui():
    """
    Sends a command from the command entry widget to the serial device.
    """
    command = ctx.command_entry.get()
    send_command(command)
    display_user_command(command)
    ctx.command_entry.delete(0, tk.END)

def send_permanent_command_ui(entry):
    """
    Sends a command from a permanent command entry widget to the serial device.

    Args:
        entry (tk.Entry): The entry widget containing the command.
    """
    command = entry.get()
    send_command(command)
    display_user_command(command)

def display_user_command(command):
    """
    Displays a user's command in the data display.

    Args:
        command (str): The command to display.
    """
    user_command = f"user > {command}\n"
    ctx.data_display.insert(tk.END, user_command, 'user')
    ctx.data_display.see(tk.END)

def display_data(data):
    """
    Displays incoming data in the data display.

    Args:
        data (str): The data to display.
    """
    ctx.data_display.insert(tk.END, data)
    ctx.data_display.see(tk.END)

def reset_data():
    """
    Resets the data and clears the data display and plot.
    """
    ctx.x_coords.clear()
    ctx.y_coords.clear()
    ctx.data_display.delete('1.0', tk.END)
    if ctx.graph_window and ctx.graph_window.winfo_exists():
        update_graph(ctx.x_coords, ctx.y_coords, ctx.lines, ctx.ax, ctx.fig)

def toggle_graph():
    """
    Toggles the visibility of the graph window.
    """
    if ctx.graph_window is None or not ctx.graph_window.winfo_exists():
        ctx.graph_window, ctx.canvas, ctx.lines, ctx.ax, ctx.fig = create_plot_window(ctx.x_coords, ctx.y_coords)
        ctx.graph_button.config(text="Hide Graph")
    else:
        close_plot_window(ctx.graph_window, ctx.canvas)
        ctx.graph_window = None
        ctx.graph_button.config(text="Show Graph")

def update_plot_config_ui():
    """
    Updates the plot configuration based on the values from the UI entries.
    """
    x_column = ctx.x_column_entry.get()
    y_columns = ctx.y_columns_entry.get().split(',')
    
    # Update the x_column in plot_config
    if x_column.strip().lower() == 'none' or not x_column.strip():
        plot_config["x_column"] = None
    else:
        plot_config["x_column"] = int(x_column)
    
    # Update the y_columns in plot_config
    plot_config["y_columns"] = [int(col) for col in y_columns if col.strip() and col.strip().lower() != 'none']
    
    if ctx.graph_window and ctx.graph_window.winfo_exists():
        close_plot_window(ctx.graph_window, ctx.canvas)
        ctx.graph_window = None
        ctx.graph_button.config(text="Show Graph")
    
    reset_data()  # Reset data before updating plot
    update_plot_config()  # Update plot configuration

def update_plot(root):
    """
    Updates the plot with new data from the data queue.

    Args:
        root (tk.Tk): The Tkinter root window.
    """
    if root.winfo_exists():
        while not data_queue.empty():
            data = data_queue.get()
            display_data(data)
            try:
                x, y_values = parse_data(data)
                if x is not None:
                    ctx.x_coords.append(x)
                else:
                    ctx.x_coords.append(len(ctx.x_coords))

                for i, y in enumerate(y_values):
                    if len(ctx.y_coords) <= i:
                        ctx.y_coords.append([])
                    ctx.y_coords[i].append(y)

                if ctx.graph_window and ctx.graph_window.winfo_exists():
                    update_graph(ctx.x_coords, ctx.y_coords, ctx.lines, ctx.ax, ctx.fig)
            except ValueError as e:
                print(f"ValueError: {e}")
            except IndexError as e:
                print(f"IndexError: {e}")
            except Exception as e:
                print(f"Unexpected error: {e}")
        root.after(100, lambda: update_plot(root))
        
def text_button_action():
    """
    Handles the text button action. Toggles the text display in the data display.
    """
    if ctx.text_button.config('text')[-1] == 'Open Text':
        ctx.text_window = tk.Toplevel()
        ctx.text_window.title("Text Window")

        # Create the entry widget for multiline input
        ctx.text_entry = tk.Text(ctx.text_window, height=10, width=40)
        ctx.text_entry.pack(pady=5)
        
        if "final_text" in ctx.global_config:
            if ctx.global_config["final_text"]:
                ctx.text_entry.insert("1.0", ctx.global_config["final_text"])  # Use "1.0" as the starting index

        # Create the checkbutton to decide whether to clear the text after sending
        ctx.clear_text_var = tk.BooleanVar(value=False)
        ctx.clear_text_checkbutton = tk.Checkbutton(ctx.text_window, text="Clear text after sending", variable=ctx.clear_text_var)
        ctx.clear_text_checkbutton.pack(pady=5)

        # Create the send button
        ctx.send_button = tk.Button(ctx.text_window, text="Send", command=send_text_command)
        ctx.send_button.pack(pady=5)
        
        ctx.text_window.protocol("WM_DELETE_WINDOW", close_text_window)

        ctx.text_button.config(text='Close Text')
    else:
        close_text_window()

            
def send_text_command():
    """
    Sends the text from the multiline entry widget to the USART.
    """
    text = ctx.text_entry.get("1.0", tk.END).strip()  # Get all text from the Text widget
    command = text.replace("\n", "\n, ")  # Format the text with newlines and commas

    send_command(command)  # Send the command via USART
    display_user_command(command)

    if ctx.clear_text_var.get():
        ctx.text_entry.delete("1.0", tk.END)  # Clear the text if the checkbox is checked
        
def close_text_window():
    if ctx.text_window is not None:
        ctx.final_text = ctx.text_entry.get("1.0", tk.END).strip()
        ctx.global_config["final_text"] = ctx.final_text
        ctx.text_window.destroy()
        ctx.text_button.config(text='Open Text')