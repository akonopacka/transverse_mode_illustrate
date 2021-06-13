import numpy as np

import PySimpleGUI as sg
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.tri as tri
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)

import tkinter

from generate_charts import besselmode, get_chart
matplotlib.use("TkAgg")

# Global variables
_lambda = 0.9
_a = 10
_NA = 0.1
_charts = []

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
    for c in _charts:
        c.get_tk_widget().pack_forget()
    figures = get_chart(lambda_, a, NA)
    print(figures, "\n")
   
    draw_figures(window["-CANVAS-"].TKCanvas, figures)


def draw_figures(canvas, figures):

    counter = 0
    row = 0
    for fig in figures:
        row_ = int(counter/5)
        figure_canvas_agg = FigureCanvasTkAgg(fig, canvas)
        figure_canvas_agg.get_tk_widget().grid(row=row_, column=counter%5, padx=5, pady=5)
        figure_canvas_agg.draw()

        _charts.append(figure_canvas_agg)
        counter = counter + 1



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
    "Projekt SOIB",
    layout,
    location=(0, 0),
    size=(1900, 900),
    finalize=True,
    element_justification="center",
    font="Helvetica 16",
    resizable=True,
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
        get_mode_field_figure(_lambda, _a, _NA)

window.close()

print("Symulacja zakończona")
