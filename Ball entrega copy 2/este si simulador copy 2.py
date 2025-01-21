import json
import os
import customtkinter
from tkinter import filedialog
import matplotlib.pyplot as plt
from prueba_copy_2 import simulator  # Asegúrate de que esto esté correctamente importado
import threading
import time

# Variables globales para la simulación y datos
config_data = {}  # Aquí almacenamos los datos de configuración
recorrido_data = []  # Aquí almacenamos el recorrido generado en la simulación
json_file = 'recorrido_data.json'  # El archivo JSON donde se almacenará la trayectoria
sim = None  # Variable global para el simulador

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
        global sim
        if 'config_data' in globals() and config_data:
            xml_path = config_data.get("xml_path", "Ball entrega copy\\esfera_prueba.xml")
            # Inicializa el simulador con el archivo XML cargado
            sim = simulator(xml_path)
            
            # Iniciar simulación en un hilo separado para no bloquear la interfaz
            threading.Thread(target=run_simulation, args=(sim,), daemon=True).start()

            label_status.configure(text="Simulación iniciada.", text_color="green")
        else:
            label_status.configure(text="Carga primero una configuración.", text_color="red")
    except Exception as e:
        label_status.configure(text=f"Error: {str(e)}", text_color="red")

# Función para correr la simulación y guardar datos
def run_simulation(sim):
    """Corre la simulación y actualiza el archivo JSON con los datos en tiempo real."""
    try:
        while not sim.is_finished():  # Simula mientras no haya terminado
            # Obtener los datos de la simulación
            position_data = sim.get_position_data()

            # Convertir los datos a lista y agregarlos al recorrido
            recorrido_data.append(position_data.tolist())

            # Guardar los datos en el archivo JSON
            with open(json_file, 'w') as outfile:
                json.dump(recorrido_data, outfile)

            time.sleep(1)  # Pausa de un segundo para sincronizar con la simulación
    except Exception as e:
        print(f"Error durante la simulación: {e}")

# Función para mostrar la simulación gráfica de MuJoCo
def button_show_simulation():
    """Abre la ventana gráfica de MuJoCo para mostrar la simulación."""
    try:
        if 'config_data' in globals():
            xml_path = config_data.get("xml_path", "Ball entrega copy\\esfera_prueba.xml")
            sim = simulator(xml_path)
            sim.run()
            label_status.configure(text="Simulación iniciada.", text_color="green")
        else:
            label_status.configure(text="Carga primero una configuración.", text_color="red")
    except Exception as e:
        label_status.configure(text=f"Error: {str(e)}", text_color="red")

# Función para generar la gráfica
def plot_graph():
    """Genera la gráfica usando matplotlib basándose en el recorrido de la simulación."""
    try:
        plt.ion()  # Activar el modo interactivo de matplotlib
        fig, ax = plt.subplots()  # Crear la figura y el eje de la gráfica

        # Función que actualizará la gráfica continuamente
        def update_plot():
            try:
                if os.path.exists(json_file) and os.path.getsize(json_file) > 0:
                    with open(json_file, 'r') as infile:
                        recorrido = json.load(infile)

                    # Extraer las posiciones X y Y del recorrido
                    x_positions = [pos[0] for pos in recorrido]
                    y_positions = [pos[1] for pos in recorrido]

                    # Graficar los datos
                    ax.clear()
                    ax.plot(x_positions, y_positions, marker='o', linestyle='-', color='b')
                    ax.set_title("Recorrido del Objeto")
                    ax.set_xlabel("Posición X")
                    ax.set_ylabel("Posición Y")
                    ax.grid(True)

                    plt.draw()
                    plt.pause(1)

                app.after(1000, update_plot)
            except Exception as e:
                print(f"Error al actualizar la gráfica: {e}")

        update_plot()

    except Exception as e:
        print(f"Error al generar la gráfica: {e}")

# Creación de la interfaz gráfica
app = customtkinter.CTk()
app.title("Simulador de Pelotas")
app.geometry("400x200")

# Botón para cargar el archivo de configuración
button_carga_config = customtkinter.CTkButton(app, text="Cargar Configuración", command=button_carga)
button_carga_config.grid(row=0, column=0, padx=20, pady=20)

# Botón para iniciar la simulación
button_iniciar = customtkinter.CTkButton(app, text="Iniciar Simulación", command=button_callback)
button_iniciar.grid(row=0, column=1, padx=20, pady=20)

# Botón para mostrar la simulación
button_mostrar = customtkinter.CTkButton(app, text="Mostrar Simulación", command=button_show_simulation)
button_mostrar.grid(row=1, column=0, padx=20, pady=20)

# Etiqueta para mostrar el estado de la carga o error
label_status = customtkinter.CTkLabel(app, text="Cargue un archivo de configuración para empezar.", text_color="blue")
label_status.grid(row=2, column=0, columnspan=2, padx=20, pady=10)

# Inicia el bucle de la interfaz gráfica
app.mainloop()
