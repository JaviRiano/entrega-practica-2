import json
import customtkinter
import matplotlib.pyplot as plt
from tkinter import filedialog
from prueba_copy_2 import simulator  # Asegúrate de que esto esté correctamente importado
import os

# Global variable to store configuration data
config_data = {}

# Variable global para almacenar las posiciones durante la simulación
recorrido_data = []

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

def button_callback():
    """Inicia la simulación con los datos cargados desde el archivo de configuración."""
    try:
        if 'config_data' in globals() and config_data:
            xml_path = config_data.get("xml_path", "Ball entrega copy\\esfera_prueba.xml")
            # Inicializa el simulador con el archivo XML cargado
            sim = simulator(xml_path)
            sim.run()  # Inicia la simulación
            
            # Crear la carpeta Ball entrega copy si no existe
            output_dir = "Ball entrega copy"
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            # Guardar el recorrido en un archivo JSON dentro de la carpeta Ball entrega copy
            json_path = os.path.join(output_dir, 'recorrido_data.json')
            with open(json_path, 'w') as outfile:
                json.dump(recorrido_data, outfile)
                
            label_status.configure(text="Simulación terminada. Generando gráfico...", text_color="green")
            plot_graph()  # Llama a la función para mostrar la gráfica

        else:
            label_status.configure(text="Carga primero una configuración.", text_color="red")
    except Exception as e:
        label_status.configure(text=f"Error: {str(e)}", text_color="red")

def plot_graph():
    """Genera la gráfica usando matplotlib basándose en el recorrido de la simulación."""
    try:
        # Lee los datos del archivo JSON
        json_path = os.path.join("Ball entrega copy", 'recorrido_data.json')
        with open(json_path, 'r') as infile:
            recorrido = json.load(infile)

        # Extraer las posiciones X y Y del recorrido
        x_positions = [pos[0] for pos in recorrido]
        y_positions = [pos[1] for pos in recorrido]

        # Graficar los datos
        plt.plot(x_positions, y_positions, marker='o', linestyle='-', color='b')
        plt.title("Recorrido del Objeto")
        plt.xlabel("Posición X")
        plt.ylabel("Posición Y")
        plt.grid(True)
        plt.show()

    except Exception as e:
        print(f"Error al generar la gráfica: {str(e)}")

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

# Etiqueta para mostrar el estado de la carga o error
label_status = customtkinter.CTkLabel(app, text="Cargue un archivo de configuración para empezar.", text_color="blue")
label_status.grid(row=1, column=0, columnspan=2, padx=20, pady=10)

# Inicia el bucle de la interfaz gráfica
app.mainloop()
