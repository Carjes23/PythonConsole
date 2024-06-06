"""
This module handles the creation and updating of plots using Matplotlib in a Tkinter window.
It includes functions for creating the plot window, updating the plot data, and parsing incoming data.

Functions:
    - create_plot_window: Creates and displays a new plot window.
    - close_plot_window: Closes the plot window and cleans up.
    - update_graph: Updates the plot with new data.
    - update_plot_config: Updates the plot configuration and redraws the plot.
    - recreate_plot_window: Recreates the plot window if it exists.
    - parse_data: Parses incoming data for plotting.
"""

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from handler_config import plot_config
import ui_context as ctx
import re

def create_plot_window(x_coords, y_coords):
    """
    Creates and displays a new plot window with the given x and y coordinates.

    Args:
        x_coords (list): List of x coordinates.
        y_coords (list of lists): List of y coordinate lists for multiple lines.

    Returns:
        tuple: The created plot window, canvas, lines, axis, and figure.
    """
    fig, ax = plt.subplots()
    lines = []
    for i, y in enumerate(y_coords):
        line, = ax.plot(x_coords, y, label=f"Column{plot_config['y_columns'][i]+1}")
        lines.append(line)
    
    try:
        ax.legend()
    except Exception as e:
        print(f"Legend Error: {e}")

    graph_window = tk.Toplevel()
    graph_window.title("Plot Window")
    
    canvas = FigureCanvasTkAgg(fig, master=graph_window)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    
    graph_window.protocol("WM_DELETE_WINDOW", lambda: close_plot_window(graph_window, canvas))
    
    ctx.graph_window = graph_window
    ctx.canvas = canvas
    ctx.lines = lines
    ctx.ax = ax
    ctx.fig = fig

    return graph_window, canvas, lines, ax, fig

def close_plot_window(graph_window, canvas):
    """
    Closes the plot window and cleans up.

    Args:
        graph_window (tk.Toplevel): The plot window to close.
        canvas (FigureCanvasTkAgg): The canvas to clean up.
    """
    if graph_window is not None:
        ctx.graph_button.config(text="Show Graph")
        canvas.get_tk_widget().pack_forget()
        graph_window.destroy()

def update_graph(x_coords, y_coords, lines, ax, fig):
    """
    Updates the plot with new data.

    Args:
        x_coords (list): List of x coordinates.
        y_coords (list of lists): List of y coordinate lists for multiple lines.
        lines (list): List of line objects to update.
        ax (matplotlib.axes.Axes): The axis to update.
        fig (matplotlib.figure.Figure): The figure to update.
    """
    for i, y in enumerate(y_coords):
        if i < len(lines):
            lines[i].set_xdata(x_coords)
            lines[i].set_ydata(y)
    ax.relim()
    ax.autoscale_view()
    fig.canvas.draw_idle()

def update_plot_config():
    """
    Updates the plot configuration and redraws the plot.
    """
    if ctx.graph_window and ctx.graph_window.winfo_exists():
        ctx.ax.clear()
        ctx.lines = []
        for i, y in enumerate(ctx.y_coords):
            line, = ctx.ax.plot(ctx.x_coords, y, label=f"Column{plot_config['y_columns'][i]+1}")
            ctx.lines.append(line)
        try:
            ctx.ax.legend()
        except Exception as e:
            print(f"Legend Error: {e}")
        ctx.fig.canvas.draw_idle()

def recreate_plot_window():
    """
    Recreates the plot window if it exists.
    """
    if ctx.graph_window and ctx.graph_window.winfo_exists():
        close_plot_window(ctx.graph_window, ctx.canvas)  # Close existing plot window
    ctx.graph_window, ctx.canvas, ctx.lines, ctx.ax, ctx.fig = create_plot_window(ctx.x_coords, ctx.y_coords)  # Create a new plot window

def parse_data(data):
    """
    Parses incoming data for plotting.

    Args:
        data (str): The incoming data as a string.

    Returns:
        tuple: The parsed x value and a list of parsed y values.
    """
    parts = data.strip().split('\t')
    x_column = plot_config.get("x_column")
    y_columns = plot_config.get("y_columns", [])

    def extract_number(part):
        match = re.search(r'[-+]?\d*\.?\d+', part)
        return float(match.group()) if match else None

    if not parts:
        return None, []

    x = None
    if x_column is not None and 0 <= x_column < len(parts):
        x = extract_number(parts[x_column])

    y_values = []
    for col in y_columns:
        if 0 <= col < len(parts):
            number = extract_number(parts[col])
            if number is not None:
                y_values.append(number)

    return x, y_values
