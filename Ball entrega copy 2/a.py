import customtkinter
from tkinter import filedialog
import json
import os
from prueba import simulator
from c import Grafica

def button_carga():
    filepath = filedialog.askopenfilename(
        title="Selecciona el archivo de configuración",
        filetypes=[("Archivos JSON", "*.json"), ("Todos los archivos", "*.*")]
    )
    if filepath:
        with open(filepath, 'r') as f:
            config = json.load(f)
        label_status.configure(text=f"Archivo cargado: {os.path.basename(filepath)}", text_color="green")
        global config_data
        config_data = config  
    else:
        label_status.configure(text="No se seleccionó ningún archivo.", text_color="red")


def button_callback():
    try:
        if 'config_data' in globals():
            xml_path = config_data.get("xml_path", "Ball entrega copy\\esfera_prueba.xml")
            
            # Inicializar la gráfica y pasarla al simulador
            grafica = Grafica()
            sim = simulator(xml_path, grafica)
            
            # Iniciar la simulación
            label_status.configure(text="Simulación iniciada.", text_color="green")
            
            # Ejecutar la simulación y pasar las posiciones a la gráfica
            sim.run()
            
            # Después de la simulación, iniciar la gráfica
            grafica.iniciar()
        else:
            label_status.configure(text="Carga primero una configuración.", text_color="red")
    except Exception as e:
        label_status.configure(text=f"Error: {str(e)}", text_color="red")


# Configuración de la interfaz
app = customtkinter.CTk()
app.title("Simulador de Pelotas")
app.geometry("400x200")

button_carga_config = customtkinter.CTkButton(app, text="Cargar Configuración", command=button_carga)
button_carga_config.grid(row=0, column=0, padx=20, pady=20)

button_iniciar = customtkinter.CTkButton(app, text="Iniciar Simulación", command=button_callback)
button_iniciar.grid(row=0, column=1, padx=20, pady=20)

label_status = customtkinter.CTkLabel(app, text="Cargue un archivo de configuración para empezar.", text_color="blue")
label_status.grid(row=1, column=0, columnspan=2, padx=20, pady=10)

app.mainloop()
