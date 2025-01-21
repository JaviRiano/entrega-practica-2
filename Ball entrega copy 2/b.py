import json
import customtkinter
import matplotlib.pyplot as plt
from tkinter import filedialog
from prueba import simulator  # Asegúrate de que esto esté correctamente importado
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
            # Eliminar el archivo JSON al inicio de la simulación
            if os.path.exists('recorrido_data.json'):
                os.remove('recorrido_data.json')

            xml_path = config_data.get("xml_path", "Ball entrega copy\\esfera_prueba.xml")
            # Inicializa el simulador con el archivo XML cargado
            sim = simulator(xml_path)
            sim.run()  # Inicia la simulación

            # Aquí estamos suponiendo que el simulador llena `recorrido_data`
            # Necesitamos confirmar que los datos están siendo guardados en la lista
            print(f"Datos de recorrido: {recorrido_data}")  # Debug: Ver los datos recolectados
            if recorrido_data:  # Verifica si hay datos de recorrido
                with open('recorrido_data.json', 'w') as outfile:
                    json.dump(recorrido_data, outfile)
                label_status.configure(text="Simulación terminada. Generando gráfico...", text_color="green")
                plot_graph()  # Llama a la función para mostrar la gráfica
            else:
                label_status.configure(text="No se generaron datos de recorrido.", text_color="red")
        else:
            label_status.configure(text="Carga primero una configuración.", text_color="red")
    except Exception as e:
        label_status.configure(text=f"Error: {str(e)}", text_color="red")

def plot_graph():
    """Genera la gráfica usando matplotlib basándose en el recorrido de la simulación."""
    try:
        # Verifica que el archivo JSON existe
        if os.path.exists('recorrido_data.json'):
            with open('recorrido_data.json', 'r') as infile:
                recorrido = json.load(infile)

            # Verificar si los datos del recorrido son válidos
            if not recorrido:
                raise ValueError("No se encontraron datos de recorrido en el archivo JSON.")
            
            # Extraer las posiciones X y Y del recorrido
            x_positions = [pos[0] for pos in recorrido]
            y_positions = [pos[1] for pos in recorrido]

            # Graficar los datos con colores personalizados
            plt.figure(figsize=(8, 6))

            # Línea de recorrido en color azul, con puntos naranjas
            plt.plot(x_positions, y_positions, marker='o', linestyle='-', color='blue', markersize=6, label="Recorrido")

            # Títulos y etiquetas con color personalizado
            plt.title("Recorrido del Objeto en la Simulación", fontsize=14, color='purple')
            plt.xlabel("Posición X", fontsize=12, color='darkgreen')
            plt.ylabel("Posición Y", fontsize=12, color='darkgreen')

            # Fondo y ejes con colores personalizados
            plt.grid(True, color='gray', linestyle='--', linewidth=0.5)
            plt.gca().set_facecolor('lightgray')
            plt.gca().spines['top'].set_color('black')
            plt.gca().spines['bottom'].set_color('black')
            plt.gca().spines['left'].set_color('black')
            plt.gca().spines['right'].set_color('black')

            # Leyenda
            plt.legend(loc="upper right")

            # Mostrar la gráfica
            plt.show()
        else:
            label_status.configure(text="No se encontró el archivo JSON para la gráfica.", text_color="red")

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

