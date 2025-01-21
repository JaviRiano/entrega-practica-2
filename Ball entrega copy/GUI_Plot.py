
import customtkinter
import json
import threading
import tkinter.messagebox
from datetime import datetime
import customtkinter as ctk
import numpy as np
import random

customtkinter.set_appearance_mode("dark")


# main windows
root = customtkinter.CTk()
root.title("NN")
root.geometry("1280x720")
#root.bind("<Return>", on_enter_key)

# configure grid layout (4x4)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure((2, 3), weight=0)
root.grid_rowconfigure((0, 1, 2), weight=1)


line_color = "#A9BCD0"
line2_color = "#4E5973"
draw_color = "#58A4B0"
background_color = "#373F51"

# Plot Size 800x800 
canvas_width = 640
canvas_height = 400
center_x = canvas_width // 2
center_y = canvas_height // 2
canvas = customtkinter.CTkCanvas(root, width=canvas_width, height=canvas_height, bg=background_color)
canvas.grid(row=0, column=0, padx=20, pady=20)

# Etiqueta para mostrar el video
sidebar_frame_diagnostic = customtkinter.CTkFrame(root, width=1, corner_radius=0)
sidebar_frame_diagnostic.grid(row=0, column=1, padx=5, pady=20, rowspan=1, sticky="ne")
camera_label = ctk.CTkLabel(root, text="")
camera_label.grid(row=0, column=2, padx=0, pady=0)


#vid = cv2.VideoCapture(0)

is_mouse_pressed = False
moving_ctrl_flag = False
capture_running = False
serial_status = False
capture_running_fcg = False
ret = False

ser = None

current_sent_y = 0
current_sent_z = 200

# Variables globales
data = []

time_data = 0
line_last_x = 0
line_last_y = 0

current_x = 0
current_y = 0

slidevalue = 50

tCapture = 60


def getTime():
    # Obtener la fecha y hora actuales
    now = datetime.now()
    # Obtener el día de la semana
    day_of_week = now.strftime("%A")
    # Obtener la fecha en formato YYYY-MM-DD
    date = now.strftime("%Y-%m-%d")
    # Obtener la hora en formato HH:MM:SS
    time = now.strftime("%H:%M:%S")
    # Unir todo en un solo string
    combined_string = f"Day: {day_of_week}, Date: {date}, Time: {time}"
    return combined_string

#-----------------------------------------------------------
# Plot Signals
#-----------------------------------------------------------
def map_value(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

# Función para actualizar el gráfico
def update_plot():
    global data, line_last_x, line_last_y, time_data
    
    try:
        if data:
            time = np.linspace(0, len(data) - 1, len(data))

            data_value = data[time_data]
            canvas.create_line(0 + line_last_x, center_y - line_last_y, 0 + time_data, center_y - data_value, fill=draw_color, width=1)
            line_last_x = time_data
            line_last_y = data_value
            time_data = time_data + 1
            if time_data == canvas_width:
                time_data = 0
                line_last_x = 0
                line_last_y = 0
                clear_lines()
    except:
        pass

    root.after(1, update_plot)  # Actualizar cada 100 ms'''

def clear_lines():
    canvas.delete("all")
    draw_axis()

def draw_axis():

    min_x_axis = 0
    max_x_axis = canvas_width

    min_y_axis = -3.3
    max_y_axis = 3.3

    # Vertical Grid
    for x_grid in range(0, canvas_width, 10):
        canvas.create_line(x_grid, 0, x_grid, canvas_height, fill=line2_color, width=1)
    # Horizontal Grid
    for y_grid in range(0, canvas_height, 10):
        canvas.create_line(0, y_grid, canvas_width, y_grid, fill=line2_color, width=1)
    canvas.create_line(min_x_axis, 0, min_x_axis, canvas_height, fill=line_color, width=1)
    canvas.create_line(0, center_y, canvas_width, center_y, fill=line_color, width=1)
    # Eje X
    for iX in range(10, canvas_width, 50):
        canvas.create_text(min_x_axis+30+iX, center_y+8, text=str(iX), fill=line_color, anchor='e')    
    # Eje Y
    for iY in range(0, canvas_height, 50):
        canvas.create_text(min_x_axis+30, center_y+8-iY, text=str(iY), fill=line_color, anchor='e')
        canvas.create_text(min_x_axis+30, center_y+8+iY, text="-" + str(iY), fill=line_color, anchor='e')


#-----------------------------------------------------------
# Interaction Events
#-----------------------------------------------------------

def on_mouse_motion(event):
    global line_last_x, line_last_y
    pass
        
def on_mouse_press(event):
    global is_mouse_pressed

    is_mouse_pressed = True

def on_mouse_release(event):
    global is_mouse_pressed, line_last_x, line_last_y

    is_mouse_pressed = False

def sidebar_button_event():
    print("sidebar_button click")

def change_appearance_mode_event(new_appearance_mode: str):
    customtkinter.set_appearance_mode(new_appearance_mode)

def change_scaling_event(new_scaling: str):
    new_scaling_float = int(new_scaling.replace("%", "")) / 100
    customtkinter.set_widget_scaling(new_scaling_float)    


# Función para leer datos 
def thread_data():
    global data, capture_running, ser
    while True:
        position = random.uniform(-10, 10)
        value = float(position)
        data.append(value)
        if len(data) > canvas_width:  # Mantener solo los últimos 100 valores
            data.pop(0)



# Función para iniciar la captura
def start_simulation():
    print("Init-Sim")
    threading.Thread(target=thread_data, daemon=True).start()
    update_plot() 

#-----------------------------------------------------------
# create sidebar frame with widgets
#-----------------------------------------------------------
sidebar_frame = customtkinter.CTkFrame(root, width=20, corner_radius=0)
sidebar_frame.grid(row=1, column=0, padx=20, pady=2, rowspan=1, columnspan=1, sticky="w")
sidebar_frame.grid_rowconfigure(4, weight=1)

draw_axis()

capture_ecg = customtkinter.CTkButton(sidebar_frame, command=start_simulation, text="Iniciar Simulacion")
capture_ecg.grid(row=1, column=0, padx=20, pady=5)

root.mainloop()
