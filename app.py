import numpy as np

import PySimpleGUI as sg
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.tri as tri
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from generate_charts import besselmode, get_chart
matplotlib.use("TkAgg")

# Global variables
_lambda = 0.9
_a = 10
_NA = 0.1


def check_input_values(values):

    global _lambda
    global _a
    global _NA

    lambda_ = values['-LAMBDA-']
    a = values['-A-']
    NA = values['-NA-']

    try:
        _lambda = float(lambda_)
        _a = float(a)
        _NA = float(NA)
    except:
        print("Input values couldn't be converted.")
        return False

    return True


def get_mode_field_figure(lambda_, a, NA):
    fig = get_chart(lambda_, a, NA)
    return fig


def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side="top", fill="both", expand=1)
    return figure_canvas_agg


# Define the window layout
layout = [
    [sg.Text("Rozkład natężenia pola w przekroju poprzecznym \n w skokowym światłowodzie cylindrycznym",  font="Helvetica 26")],
    [sg.Text("")],
    [sg.Text("Lambda: "),sg.Input('0.9', key='-LAMBDA-', size =(10, 1)), sg.Text("µm   "), sg.Text("NA: "),sg.Input('0.1', key='-NA-', size =(10, 1)), sg.Text("    a - średnica rdzenia: "),sg.Input('10', key='-A-', size =(10, 1)), sg.Text("µm ")],  
    [sg.Text("",key='-INFO-')],
    [sg.Canvas(key="-CANVAS-")],
    [sg.Button("Symulacja"), sg.Button('Zakoncz')],
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


not_finished = True
while not_finished:
    event, values = window.read()
    # See if user wants to quit or window was closed
    if event == sg.WINDOW_CLOSED or event == 'Zakoncz':
        not_finished = False
        break

    if event == "Symulacja":
        is_valid = check_input_values(values)
        draw_figure(window["-CANVAS-"].TKCanvas, get_mode_field_figure(_lambda, _a, _NA))

window.close()

print("Symulacja zakończona")
