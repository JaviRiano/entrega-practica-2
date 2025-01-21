import mujoco as mj
import glfw
import numpy as np
import pickle  # Para guardar la trayectoria en un archivo

class Simulator:
    def __init__(self, path):
        self.window = None
        self.model = None
        self.data = None
        self.object_id = None
        self.x_positions = []  # Para almacenar las posiciones
        self.y_positions = []
        self.z_positions = []
        self.body_name = "sphere2"
        
        self.init_simulation(path)

    def init_simulation(self, path):
        if not glfw.init():
            raise RuntimeError("Failed to initialize GLFW")

        self.window = glfw.create_window(1200, 900, "Simulador MuJoCo", None, None)
        if not self.window:
            glfw.terminate()
            raise RuntimeError("Failed to create GLFW window")
        
        glfw.make_context_current(self.window)
        
        # Cargar el modelo
        self.model = mj.MjModel.from_xml_path(path)
        self.data = mj.MjData(self.model)

        # Obtener el ID del objeto
        self.object_id = mj.mj_name2id(self.model, mj.mjtObj.mjOBJ_BODY, self.body_name)
    
    def record_position(self):
        """
        Graba la posición de la esfera en cada paso de la simulación.
        """
        xpos = self.data.body_xpos[self.object_id]
        self.x_positions.append(xpos[0])
        self.y_positions.append(xpos[1])
        self.z_positions.append(xpos[2])

    def run(self):
        while not glfw.window_should_close(self.window):
            mj.mj_step(self.model, self.data)
            mj.mj_forward(self.model, self.data)
            
            # Grabar la posición en cada paso
            self.record_position()

            # Visualizar la simulación
            mj.mjv_updateScene(self.model, self.data, mj.MjvOption(), None, mj.MjvCamera(), 0, None)
            mj.mjr_render(mj.MjrRect(0, 0, 1200, 900), None, None)

            glfw.swap_buffers(self.window)
            glfw.poll_events()

        glfw.terminate()

        # Guardar la trayectoria cuando la simulación termina
        self.save_trajectory()

    def save_trajectory(self):
        """
        Guarda las posiciones de la trayectoria en un archivo binario usando pickle.
        """
        with open('trajectory.pkl', 'wb') as f:
            pickle.dump((self.x_positions, self.y_positions, self.z_positions), f)
        print("Trayectoria guardada en 'trajectory.pkl'.")

# Crear e iniciar la simulación
sim = Simulator("Ball entrega copy\\esfera_prueba.xml")
sim.run()
