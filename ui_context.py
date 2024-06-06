"""
ui_context.py

This module defines the global UI context for the Microcontroller Interface application.
It includes references to various Tkinter widgets and other context-specific variables
used throughout the application.

Attributes:
    port_selector (tk.Widget): The widget for selecting the serial port.
    baudrate_entry (tk.Entry): The entry widget for the baud rate.
    connect_button (tk.Button): The button to connect/disconnect the serial connection.
    command_entry (tk.Entry): The entry widget for sending commands.
    data_display (tk.Widget): The widget to display received data.
    graph_button (tk.Button): The button to open the graph window.
    graph_window (tk.Toplevel): The window displaying the graph.
    x_column_entry (tk.Entry): The entry widget for the x-axis column configuration.
    y_columns_entry (tk.Entry): The entry widget for the y-axis columns configuration.
    x_coords (list): The list of x coordinates for plotting.
    y_coords (list of lists): The list of y coordinate lists for plotting.
    lines (list): The list of line objects in the plot.
    ax (matplotlib.axes.Axes): The axis object for the plot.
    fig (matplotlib.figure.Figure): The figure object for the plot.
    canvas (FigureCanvasTkAgg): The canvas for displaying the Matplotlib figure in Tkinter.
"""

port_selector = None
baudrate_entry = None
connect_button = None
command_entry = None
data_display = None
graph_button = None
graph_window = None
x_column_entry = None
y_columns_entry = None
x_coords = []
y_coords = []
lines = []
ax = None
fig = None
canvas = None
