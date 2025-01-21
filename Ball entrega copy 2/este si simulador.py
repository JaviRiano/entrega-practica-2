import json
import os
import customtkinter as ctk
from tkinter import filedialog
import matplotlib.pyplot as plt
from prueba_copy_2 import simulator  # Asegúrate de que esto esté correctamente importado
import threading
import time

# Variables globales para la simulación y datos
config_data = {}  # Aquí almacenamos los datos de configuración
recorrido_data = []  # Aquí almacenamos el recorrido generado en la simulación
json_file = 'recorrido_data.json'  # El archivo JSON donde se almacenará la trayectoria
sim_thread = None  # Variable para mantener el hilo de simulación

# Función para cargar el archivo de configuración
def button_carga():
    """Abre un diálogo de archivos para seleccionar el archivo de configuración."""
    filepath = filedialog.askopenfilename(
        title="Selecciona el archivo de configuración",
        filetypes=[("Archivos JSON", "*.json"), ("Todos los archivos", "*.*")]
    )
    if filepath:
        try:
            with open(filepath, 'r') as f:
                config = json.load(f)
            label_status.configure(text=f"Archivo cargado: {os.path.basename(filepath)}", text_color="green")
            global config_data
            config_data = config  
        except Exception as e:
            label_status.configure(text=f"Error al cargar el archivo: {str(e)}", text_color="red")
    else:
        label_status.configure(text="No se seleccionó ningún archivo.", text_color="red")

# Función para iniciar la simulación
def button_callback():
    """Inicia la simulación con los datos cargados desde el archivo de configuración."""
    try:
        if 'config_data' in globals() and config_data:
            xml_path = config_data.get("xml_path", "Ball entrega copy\\esfera_prueba.xml")
            # Inicializa el simulador con el archivo XML cargado
            sim = simulator(xml_path)
            global sim_thread
            sim_thread = threading.Thread(target=run_simulation, args=(sim,))
            sim_thread.start()  # Inicia el hilo de la simulación
            label_status.configure(text="Simulación iniciada.", text_color="green")

            # Inicia el proceso de guardar datos cada segundo en un hilo separado
            threading.Thread(target=update_json_periodically, args=(sim,), daemon=True).start()
            

        else:
            label_status.configure(text="Carga primero una configuración.", text_color="red")
    except Exception as e:
        label_status.configure(text=f"Error: {str(e)}", text_color="red")

# Función que ejecuta la simulación
def run_simulation(sim):
    """Ejecuta la simulación en un hilo separado."""
    try:
        sim.run()  # Inicia la simulación
        label_status.configure(text="Simulación terminada.", text_color="green")
    except Exception as e:
        label_status.configure(text=f"Error al ejecutar simulación: {str(e)}", text_color="red")

# Función para actualizar el archivo JSON cada segundo
def update_json_periodically(sim):
    """Actualiza el archivo JSON cada segundo con los nuevos datos de la simulación."""
    try:
        while sim_thread.is_alive():  # Verifica si el hilo de simulación sigue activo
            # Recoger los datos de la simulación
            position_data = sim.get_position_data()  # Obtener los datos actuales de la simulación
            position_data = position_data.tolist()

            # Añadir el nuevo dato al recorrido
            recorrido_data.append(position_data)

            # Guardar los datos en el archivo JSON (agregar nuevos datos sin sobrescribir)
            with open(json_file, 'w') as outfile:
                # Escribir todos los datos de recorrido en el archivo JSON de una sola vez
                json.dump(recorrido_data, outfile)

            # Esperar 1 segundo antes de continuar
            time.sleep(1)
        
        # Cuando termine la simulación, seguimos actualizando el JSON una última vez
        with open(json_file, 'w') as outfile:
            json.dump(recorrido_data, outfile)
            
    except Exception as e:
        print(f"Error al actualizar el archivo JSON: {e}")

# Función para generar la gráfica después de la simulación
def plot_graph():
    """Genera la gráfica usando matplotlib basándose en el recorrido de la simulación."""
    try:
        plt.ion()  # Activar el modo interactivo de matplotlib
        fig, ax = plt.subplots()  # Crear la figura y el eje de la gráfica

        # Leer el archivo JSON y cargar los datos
        if os.path.exists(json_file) and os.path.getsize(json_file) > 0:
            with open(json_file, 'r') as infile:
                recorrido = json.load(infile)

            # Extraer las posiciones X y Y del recorrido
            x_positions = [pos[0] for pos in recorrido]
            y_positions = [pos[1] for pos in recorrido]

            # Graficar los datos
            ax.plot(x_positions, y_positions, marker='o', linestyle='-', color='b')
            ax.set_title("Recorrido del Objeto")
            ax.set_xlabel("Posición X")
            ax.set_ylabel("Posición Y")
            ax.grid(True)

            plt.show()  # Mostrar la gráfica

        else:
            label_status.configure(text="No hay datos disponibles para graficar.", text_color="red")
    except Exception as e:
        print(f"Error al generar la gráfica: {e}")

# Función para finalizar y graficar después de que se hayan guardado los datos
def show_graph_after_simulation():
    """Muestra la gráfica después de que los datos hayan sido guardados."""
    plot_graph()
    label_status.configure(text="Gráfico mostrado.", text_color="green")

# Creación de la interfaz gráfica
app = ctk.CTk()
app.title("Simulador de Pelotas")
app.geometry("400x200")

# Botón para cargar el archivo de configuración
button_carga_config = ctk.CTkButton(app, text="Cargar Configuración", command=button_carga)
button_carga_config.grid(row=0, column=0, padx=20, pady=20)

# Botón para iniciar la simulación
button_iniciar = ctk.CTkButton(app, text="Iniciar Simulación", command=button_callback)
button_iniciar.grid(row=0, column=1, padx=20, pady=20)

# Botón para graficar después de la simulación
button_graficar = ctk.CTkButton(app, text="Mostrar Gráfico", command=show_graph_after_simulation)
button_graficar.grid(row=1, column=0, columnspan=2, padx=20, pady=20)

# Etiqueta para mostrar el estado de la carga o error
label_status = ctk.CTkLabel(app, text="Cargue un archivo de configuración para empezar.", text_color="blue")
label_status.grid(row=2, column=0, columnspan=2, padx=20, pady=10)

# Inicia el bucle de la interfaz gráfica
app.mainloop()

