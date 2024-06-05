import tkinter as tk
import threading
from ui_setup import setup_ui
from ui_handlers import update_plot
from serial_handler import read_serial, connect_serial, disconnect_serial
from handler_config import write_config, permanent_command_entries

def main():
    global stop_event, serial_thread, root, x_column_entry, y_columns_entry

    root = tk.Tk()
    root.title("Microcontroller Interface")

    x_column_entry, y_columns_entry = setup_ui(root, connect_serial, disconnect_serial)

    stop_event = threading.Event()
    serial_thread = threading.Thread(target=read_serial, args=(stop_event,))
    serial_thread.start()

    def save_config():
        config = {}
        for i, entry in enumerate(permanent_command_entries):
            config[f"permanent_command_{i+1}"] = entry.get()
        
        # Save plot configuration
        x_column = x_column_entry.get()
        y_columns = y_columns_entry.get().split(',')
        config["x_column"] = int(x_column) if x_column else None
        config["y_columns"] = [int(col) for col in y_columns if col]
        
        write_config(config)

    def on_closing():
        stop_event.set()
        disconnect_serial()
        save_config()
        root.quit()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.after(100, lambda: update_plot(root))
    root.mainloop()

if __name__ == "__main__":
    main()
