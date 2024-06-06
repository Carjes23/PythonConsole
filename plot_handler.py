import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from handler_config import plot_config
import ui_context as ctx
import re

def create_plot_window(x_coords, y_coords):
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
    graph_window.title("Graph")
    
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
    if graph_window is not None:
        canvas.get_tk_widget().pack_forget()
        graph_window.destroy()

def update_graph(x_coords, y_coords, lines, ax, fig):
    for i, y in enumerate(y_coords):
        if i < len(lines):
            lines[i].set_xdata(x_coords)
            lines[i].set_ydata(y)
    ax.relim()
    ax.autoscale_view()
    fig.canvas.draw_idle()

def update_plot_config():
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
    if ctx.graph_window and ctx.graph_window.winfo_exists():
        close_plot_window(ctx.graph_window, ctx.canvas)  # Close existing plot window
    ctx.graph_window, ctx.canvas, ctx.lines, ctx.ax, ctx.fig = create_plot_window(ctx.x_coords, ctx.y_coords)  # Create a new plot window

def parse_data(data):
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
