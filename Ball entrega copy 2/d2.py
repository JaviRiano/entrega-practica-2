import customtkinter as ctk
from tkinter import filedialog
import json
import os
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from prueba_copy_2 import simulator

# Función para cargar la configuración desde un archivo JSON
def button_carga(app):
    filepath = filedialog.askopenfilename(
        title="Selecciona el archivo de configuración",
        filetypes=[("Archivos JSON", "*.json"), ("Todos los archivos", "*.*")]
    )
    if filepath:
        with open(filepath, 'r') as f:
            config = json.load(f)
        app.label_status.configure(text=f"Archivo cargado: {os.path.basename(filepath)}", text_color="green")
        global config_data
        config_data = config
    else:
        app.label_status.configure(text="No se seleccionó ningún archivo.", text_color="red")


# Función para ejecutar la simulación
def button_callback(app):
    try:
        if 'config_data' in globals():
            xml_path = config_data.get("xml_path", "Ball entrega copy\\esfera_prueba.xml")
            sim = simulator(xml_path)  # Aquí debería estar tu clase o función para la simulación
            sim.run()  # Ejecución de la simulación
            app.label_status.configure(text="Simulación iniciada.", text_color="green")
            run_plot_in_main_thread(app)  # Inicia la actualización de la gráfica
        else:
            app.label_status.configure(text="Carga primero una configuración.", text_color="red")
    except Exception as e:
        app.label_status.configure(text=f"Error: {str(e)}", text_color="red")


# Función para leer los datos del archivo JSON generado por la simulación
def read_trajectory_from_json(file_name="trajectory.json"):
    try:
        with open(file_name, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error al leer el archivo JSON: {e}")
        return []


# Función para actualizar la gráfica
def update_graph(ax, line, file_name="trajectory.json"):
    # Leer datos desde el archivo JSON
    data = read_trajectory_from_json(file_name)

    if data:
        # Extraer los tiempos y posiciones para graficar
        times = [entry['time'] for entry in data]
        positions = [entry['position'][0] for entry in data]  # Graficar la posición X (puedes cambiar a Y o Z)

        # Actualizar la línea en la gráfica
        line.set_xdata(times)
        line.set_ydata(positions)

        # Redibujar la gráfica
        ax.relim()
        ax.autoscale_view()


# Función para mostrar la gráfica en tiempo real
def plot_trajectory(app, ax, line, file_name="trajectory.json"):
    # Crear la figura y los ejes
    fig, ax = plt.subplots()

    # Configuración de la gráfica
    ax.set_title("Posición del Objeto a lo largo del tiempo")
    ax.set_xlabel("Tiempo (segundos)")
    ax.set_ylabel("Posición X")
    ax.set_xlim(0, 100)  # Establecer un límite en el tiempo
    ax.set_ylim(-2, 2)   # Establecer límites para la posición

    # Inicializar una línea vacía para la gráfica
    line, = ax.plot([], [], label="Posición del objeto")

    # Insertar la gráfica en el canvas de Tkinter
    canvas = FigureCanvasTkAgg(fig, master=app.graph_frame)
    canvas.get_tk_widget().pack(fill="both", expand=True)
    canvas.draw()

    return ax, line, canvas


# Función para ejecutar la actualización periódica de la gráfica en el hilo principal
def run_plot_in_main_thread(app):
    # Crear la figura y la gráfica una sola vez
    fig, ax = plt.subplots()
    line, = ax.plot([], [], label="Posición del objeto")
    ax, line, canvas = plot_trajectory(app, ax, line)

    # Asegurarse de que el ciclo de actualización solo se realice si la ventana sigue abierta
    def update():
        if app.root.winfo_exists():  # Verifica si la ventana sigue existiendo
            update_graph(ax, line, "trajectory.json")
            canvas.draw()  # Redibuja el canvas
            update.after_id = app.root.after(1000, update)  # Llama a esta función cada 1000 ms (1 segundo)
        else:
            # Si la ventana ya no existe, cancelar la invocación y no seguir actualizando
            if hasattr(update, 'after_id'):
                app.root.after_cancel(update.after_id)
            return

    update()  # Iniciar la actualización


# Clase de la interfaz
class SimulationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Pelotas")
        self.root.geometry("800x600")

        # Configuración de la interfaz con CustomTkinter
        ctk.set_appearance_mode("System")

        # Crear un frame para la simulación y los botones
        self.simulation_frame = ctk.CTkFrame(self.root)
        self.simulation_frame.pack(pady=10, padx=10, fill="both", expand=True)

        # Crear un botón para cargar la configuración
        self.button_carga_config = ctk.CTkButton(self.simulation_frame, text="Cargar Configuración", command=lambda: button_carga(self))
        self.button_carga_config.grid(row=0, column=0, padx=20, pady=20)

        # Crear un botón para iniciar la simulación
        self.button_iniciar = ctk.CTkButton(self.simulation_frame, text="Iniciar Simulación", command=lambda: button_callback(self))
        self.button_iniciar.grid(row=0, column=1, padx=20, pady=20)

        # Etiqueta para mostrar el estado
        self.label_status = ctk.CTkLabel(self.simulation_frame, text="Cargue un archivo de configuración para empezar.", text_color="blue")
        self.label_status.grid(row=1, column=0, columnspan=2, padx=20, pady=10)

        # Crear un frame para mostrar la gráfica
        self.graph_frame = ctk.CTkFrame(self.root)
        self.graph_frame.pack(pady=20, padx=10, fill="both", expand=True)

        # Cancelar cualquier actualización pendiente cuando la ventana se cierre
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        """Cancelar todas las llamadas after() cuando la ventana se cierra."""
        if hasattr(self, 'after_id'):
            self.root.after_cancel(self.after_id)
        self.root.destroy()


# Crear la ventana principal de la interfaz
root = ctk.CTk()
app = SimulationApp(root)
root.mainloop()
