import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import mujoco as mj
import numpy as np

class GraphPlotter:
    def __init__(self, model, data):
        # Inicializar listas para almacenar las posiciones de la esfera
        self.x_positions = []
        self.y_positions = []
        self.z_positions = []
        self.model = model
        self.data = data

        # Obtener el ID del objeto "sphere2"
        self.body_name = "sphere2"
        self.object_id = mj.mj_name2id(self.model, mj.mjtObj.mjOBJ_BODY, self.body_name)
        
    def update_positions(self):
        """
        Actualiza las listas de posiciones con las coordenadas de 'sphere2'.
        Obtiene las coordenadas de 'sphere2' desde el simulador MuJoCo.
        """
        # Obtener las coordenadas globales del centro de masa de sphere2
        xpos = self.data.body_xpos[self.object_id]
        
        # Guardar las posiciones X, Y, Z
        self.x_positions.append(xpos[0])
        self.y_positions.append(xpos[1])
        self.z_positions.append(xpos[2])

    def animate(self, i):
        """
        Función de animación que actualiza la gráfica en tiempo real.
        :param i: El número de iteración de la animación.
        """
        self.update_positions()  # Actualizar las posiciones con las nuevas coordenadas
        
        ax.clear()  # Limpiar el gráfico para actualizar

        # Graficar las trayectorias X-Y y X-Z
        ax.plot(self.x_positions, self.y_positions, label="Trayectoria XY", color="blue")
        ax.plot(self.x_positions, self.z_positions, label="Trayectoria XZ", color="red")
        
        ax.set_xlabel("Posición X")
        ax.set_ylabel("Posición Y / Z")
        ax.set_title("Trayectoria de sphere2 en 2D y 3D")
        ax.legend()


def main():
    # Cargar el modelo de MuJoCo
    model = mj.MjModel.from_xml_path("Ball entrega copy\\esfera_prueba.xml")
    data = mj.MjData(model)

    # Crear una instancia de GraphPlotter
    graph_plotter = GraphPlotter(model, data)

    # Crear la figura y los ejes de la gráfica
    global ax
    fig, ax = plt.subplots()

    # Crear la animación para actualizar la gráfica
    ani = FuncAnimation(fig, graph_plotter.animate, frames=100, interval=100, repeat=False)

    # Ejecutar la simulación y actualizar la gráfica
    while True:
        mj.mj_step(model, data)  # Paso de la simulación
        mj.mj_forward(model, data)  # Avanzar el modelo

        # Mostrar la gráfica en tiempo real
        plt.pause(0.1)  # Actualizar cada 0.1 segundos para animación
        plt.draw()

    plt.show()


if __name__ == "__main__":
    main()
