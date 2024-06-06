"""
main.py

This script sets up the main interface for the Microcontroller Interface application.
It uses Tkinter for the GUI, threading for handling serial communication, and
separate modules for UI setup, plot updates, and serial handling.

Modules:
    - tkinter: For GUI components.
    - threading: For concurrent execution of the serial reading function.
    - ui_setup: Contains the setup_ui function to initialize the UI components.
    - ui_handlers: Contains the update_plot function to update the plot in the UI.
    - serial_handler: Contains functions to read from serial, connect to serial, and disconnect from serial.
    - handler_config: Contains the write_config function and permanent_command_entries list.
    - ui_context: Contains context-specific variables for the UI, such as baudrate_entry.
"""

import tkinter as tk
import threading
from ui_setup import setup_ui
from ui_handlers import update_plot
from serial_handler import read_serial, connect_serial, disconnect_serial
from handler_config import write_config, permanent_command_entries
import ui_context as ctx  # Ensure ui_context is imported

def main():
    """
    Main function to initialize the GUI, start the serial thread, and handle application exit.
    """
    global stop_event, serial_thread, root, x_column_entry, y_columns_entry

    # Initialize the main window
    root = tk.Tk()
    root.title("Microcontroller Interface")

    # Set up the UI components
    x_column_entry, y_columns_entry = setup_ui(root, connect_serial, disconnect_serial)

    # Event to signal thread termination
    stop_event = threading.Event()
    # Start the serial reading thread
    serial_thread = threading.Thread(target=read_serial, args=(stop_event,))
    serial_thread.start()

    def save_config():
        """
        Function to save the current configuration to a file.
        """
        config = {}
        for i, entry in enumerate(permanent_command_entries):
            config[f"permanent_command_{i+1}"] = entry.get()
        
        # Save plot configuration
        x_column = x_column_entry.get()
        y_columns = y_columns_entry.get().split(',')
        config["x_column"] = int(x_column) if x_column else None
        config["y_columns"] = [int(col) for col in y_columns if col]
        
        # Save baud rate
        config["baudrate"] = int(ctx.baudrate_entry.get())

        write_config(config)

    def on_closing():
        """
        Function to handle application exit.
        """
        stop_event.set()  # Signal the serial thread to stop
        disconnect_serial()  # Disconnect the serial connection
        save_config()  # Save the current configuration
        root.quit()  # Quit the Tkinter main loop
        root.destroy()  # Destroy the Tkinter window

    # Set up the window close protocol
    root.protocol("WM_DELETE_WINDOW", on_closing)
    # Schedule the plot update function
    root.after(100, lambda: update_plot(root))
    # Start the Tkinter main loop
    root.mainloop()

if __name__ == "__main__":
    main()
