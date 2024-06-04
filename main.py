import serial
import time
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import scrolledtext
import threading
import queue

def main():
    # Function to send a command to the microcontroller
    def send_command(serial_port, command):
        serial_port.write((command + '\n').encode())

    # Function to parse the received data
    def parse_data(data):
        parts = data.split('\t')
        x = float(parts[0])
        y = float(parts[1])
        return x, y

    # Set up the serial connection
    ser = serial.Serial(
        port='/dev/ttyUSB0', # Change this to the correct port for your system
        baudrate=19200,
        bytesize=serial.EIGHTBITS,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        timeout=1
    )

    # Wait for the connection to establish
    time.sleep(2)

    # Lists to store the coordinates
    x_coords = []
    y_coords = []

    plt.ion()  # Turn on interactive mode
    fig, ax = plt.subplots()
    line, = ax.plot(x_coords, y_coords, 'b-')

    data_queue = queue.Queue()

    def update_plot():
        while not data_queue.empty():
            data = data_queue.get()
            print(f"Received data: {data}")
            display_data(data)
            try:
                x, y = parse_data(data)
                x_coords.append(x)
                y_coords.append(y)
                update_graph()
            except ValueError:
                print("Error parsing data")
        root.after(100, update_plot)  # Schedule the function to run again

    def update_graph():
        line.set_xdata(x_coords)
        line.set_ydata(y_coords)
        ax.relim()
        ax.autoscale_view()
        fig.canvas.draw_idle()

    def send_command_ui():
        command = command_entry.get()
        send_command(ser, command)
        command_entry.delete(0, tk.END)

    def display_data(data):
        data_display.insert(tk.END, data + '\n')
        data_display.see(tk.END)

    def read_serial():
        while not stop_event.is_set():
            if ser.in_waiting > 0:
                data = ser.readline().decode().strip()
                data_queue.put(data)
            time.sleep(0.1)

    def reset_data():
        x_coords.clear()
        y_coords.clear()
        data_display.delete('1.0', tk.END)
        update_graph()

    # Set up the tkinter UI
    root = tk.Tk()
    root.title("Microcontroller Interface")

    frame = tk.Frame(root)
    frame.pack(padx=10, pady=10)

    command_label = tk.Label(frame, text="Enter command:")
    command_label.pack(side=tk.LEFT)

    command_entry = tk.Entry(frame, width=50)
    command_entry.pack(side=tk.LEFT, padx=5)

    send_button = tk.Button(frame, text="Send", command=send_command_ui)
    send_button.pack(side=tk.LEFT)

    reset_button = tk.Button(frame, text="Reset Data", command=reset_data)
    reset_button.pack(side=tk.LEFT, padx=5)

    data_display = scrolledtext.ScrolledText(root, width=80, height=20)
    data_display.pack(padx=10, pady=10)

    stop_event = threading.Event()
    serial_thread = threading.Thread(target=read_serial)
    serial_thread.start()

    def on_closing():
        stop_event.set()
        ser.close()
        plt.ioff()
        plt.show()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.after(100, update_plot)  # Start the update_plot function
    root.mainloop()

if __name__ == "__main__":
    main()
