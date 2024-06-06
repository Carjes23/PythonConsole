"""
serial_handler.py

This module handles serial communication with a microcontroller. It includes functions
to find available serial ports, connect to a serial port, disconnect from a serial port,
send commands, and read data from the serial port.

Functions:
    - find_serial_ports: Lists available serial ports.
    - connect_serial: Connects to a specified serial port with given parameters.
    - disconnect_serial: Disconnects the current serial connection.
    - send_command: Sends a command to the connected serial device.
    - read_serial: Continuously reads data from the serial port and adds it to a queue.
"""

import serial
import time
import queue
import serial.tools.list_ports

# Global variables for serial connection and data queue
ser = None
data_queue = queue.Queue()

def find_serial_ports():
    """
    Lists available serial ports.

    Returns:
        list: A list of available serial port device names.
    """
    ports = serial.tools.list_ports.comports()
    return [port.device for port in ports]

def connect_serial(port, baudrate):
    """
    Connects to a specified serial port with given parameters.

    Args:
        port (str): The serial port to connect to.
        baudrate (int): The baud rate for the serial connection.

    Returns:
        bool: True if connection is successful, False otherwise.
    """
    global ser
    try:
        ser = serial.Serial(
            port=port,
            baudrate=baudrate,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=1
        )
        time.sleep(2)  # Wait for the connection to establish
        return True
    except serial.SerialException as e:
        print(f"Error: {e}")
        return False
    except FileNotFoundError as e:
        print(f"FileNotFoundError: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

def disconnect_serial():
    """
    Disconnects the current serial connection.
    """
    global ser
    if ser and ser.is_open:
        ser.close()
        ser = None

def send_command(command):
    """
    Sends a command to the connected serial device.

    Args:
        command (str): The command to send.
    """
    if ser and ser.is_open:
        ser.write((command).encode())

def read_serial(stop_event):
    """
    Continuously reads data from the serial port and adds it to a queue.

    Args:
        stop_event (threading.Event): An event to signal when to stop reading.
    """
    while not stop_event.is_set():
        if ser and ser.in_waiting > 0:
            try:
                data = ser.readline().decode()
                data_queue.put(data)
            except Exception as e:
                print(f"Read error: {e}")
        time.sleep(0.1)
