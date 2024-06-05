import serial
import time
import queue
import threading
import serial.tools.list_ports

ser = None
data_queue = queue.Queue()

def find_serial_ports():
    ports = serial.tools.list_ports.comports()
    return [port.device for port in ports]

def connect_serial(port, baudrate):
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
    global ser
    if ser and ser.is_open:
        ser.close()
        ser = None

def send_command(command):
    if ser and ser.is_open:
        ser.write((command).encode())

def read_serial(stop_event):
    while not stop_event.is_set():
        if ser and ser.in_waiting > 0:
            try:
                data = ser.readline().decode()
                data_queue.put(data)
            except Exception as e:
                print(f"Read error: {e}")
        time.sleep(0.1)
