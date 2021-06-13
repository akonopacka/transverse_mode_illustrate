import numpy as np

import PySimpleGUI as sg
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.tri as tri
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from generate_charts import besselmode, get_chart


def check_input_values():
    return True


def get_mode_field_figure(lambda_, a, NA):
    fig = get_chart(lambda_, a, NA)
    return fig

matplotlib.use("TkAgg")

def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side="top", fill="both", expand=1)
    return figure_canvas_agg


# Define the window layout
layout = [
    [sg.Text("Rozkład natężenia pola w przekroju poprzecznym \n w skokowym światłowodzie cylindrycznym",  font="Helvetica 26")],
    [sg.Text("")],
    [sg.Text("Lambda: "),sg.Input(key='-LAMBDA-', size =(10, 1)), sg.Text("µm   "), sg.Text("NA: "),sg.Input(key='-NA-', size =(10, 1)), sg.Text("    R - średnica: "),sg.Input(key='-R-', size =(10, 1)), sg.Text("µm ")],  
    [sg.Text("",key='-INFO-')],
    [sg.Canvas(key="-CANVAS-")],
    [sg.Button("Symulacja"), sg.Button("Zakończ")],
]

# Create the form and show it without the plot
window = sg.Window(
    "Matplotlib Single Graph",
    layout,
    location=(0, 0),
    # margins=(100, 100),
    finalize=True,
    element_justification="center",
    font="Helvetica 16",
)


event, values = window.read()

print("Parametry symulacji:")
print(event)  
print(values)
print(values['-LAMBDA-'])
print(values['-NA-'])
print(values['-R-'])

# Add the plot to the window
draw_figure(window["-CANVAS-"].TKCanvas, get_mode_field_figure(0.9,10,0.1))

not_finished = True
while not_finished:
    event, values = window.read()

    print("Parametry symulacji:")
    print(event)  
    print(values)
    print(values['-LAMBDA-'])
    print(values['-NA-'])
    print(values['-R-'])

    # See if user wants to quit or window was closed
    if event == sg.WINDOW_CLOSED or event == 'Quit':
        not_finished = False
        break


window.close()

print("Symulacja zakończona")
