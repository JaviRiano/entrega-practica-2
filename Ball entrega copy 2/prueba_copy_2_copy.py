import mujoco as mj
from mujoco.glfw import glfw
import numpy as np
import json
import icontract

# Variables globales
mouse_x = 0
mouse_y = 0
button_left = False
object_name = 'sphere'  # Nombre del objeto a mover
body_name = "sphere"  # Nombre del cuerpo
body_id = None  # Inicializar el ID del cuerpo

# Recorrido del objeto
object_trajectory = []  # Aquí guardamos las posiciones a lo largo de la simulación

class simulator:

    # Inicialización de MuJoCo
    def __init__(self, path):
        self.button_left = False
        self.button_middle = False
        self.button_right = False
        self.lastx = 0
        self.lasty = 0

        # Inicialización de GLFW
        if not glfw.init():
            raise RuntimeError("Failed to initialize GLFW")

        # Crear ventana
        self.window = glfw.create_window(1200, 900, "MuJoCo Viewer", None, None)
        if not self.window:
            glfw.terminate()
            raise RuntimeError("Failed to create GLFW window")

        # Hacer que el contexto OpenGL sea actual
        glfw.make_context_current(self.window)
        glfw.swap_interval(1)  # Habilitar V-Sync

        # MuJoCo model y data
        self.model = mj.MjModel.from_xml_path(path)
        self.data = mj.MjData(self.model)
        self.cam = mj.MjvCamera()
        self.opt = mj.MjvOption()
        self.scene = mj.MjvScene(self.model, maxgeom=10000)
        self.context = mj.MjrContext(self.model, mj.mjtFontScale.mjFONTSCALE_150.value)

        mj.mjv_defaultCamera(self.cam)
        mj.mjv_defaultOption(self.opt)

        # Configurar callbacks de mouse
        glfw.set_key_callback(self.window, self.keyboard)
        glfw.set_cursor_pos_callback(self.window, self.mouse_move)
        glfw.set_mouse_button_callback(self.window, self.mouse_button)
        glfw.set_scroll_callback(self.window, self.scroll)

        # Obtener el ID del cuerpo
        self.body_id = mj.mj_name2id(self.model, mj.mjtObj.mjOBJ_BODY, body_name)  # Cambiar a mjOBJ_BODY para obtener el ID del cuerpo

    @icontract.require(lambda self: self.body_id is not None)  # Requiere que el ID del cuerpo sea válido
    @icontract.ensure(lambda self: len(object_trajectory) > 0)  # Asegura que haya al menos un punto registrado
    def get_position_data(self):
        """
        Recupera y valida la posición del objeto en cada paso de la simulación.
        Se asegura que las coordenadas sean válidas.
        """
        if self.body_id is not None:
            # Obtener la posición global del cuerpo
            position = self.data.body_xpos[self.body_id]  # Acceso correcto a la posición del cuerpo
            print(f"Posición del objeto {body_name}: {position}")

            # Validación defensiva
            if any(np.isnan(position)) or any(np.isinf(position)):
                raise ValueError(f"Posición inválida detectada para {body_name}: {position}")

            # Guardar la posición en el recorrido
            object_trajectory.append({
                'time': self.data.time,
                'position': position.tolist()
            })
            return position
        else:
            raise ValueError(f"Error: no se encontró el cuerpo {body_name}")

    def keyboard(self, window, key, scancode, act, mods):
        if act == glfw.PRESS and key == glfw.KEY_BACKSPACE:
            mj.mj_resetData(self.model, self.data)
            mj.mj_forward(self.model, self.data)
        for i in range(len(self.initial_joint_angles)):
            self.data.qpos[i] = self.initial_joint_angles[i]
        mj.mj_forward(self.model, self.data)

    def mouse_button(self, window, button, act, mods):
        self.button_left = (glfw.get_mouse_button(window, glfw.MOUSE_BUTTON_LEFT) == glfw.PRESS)
        self.button_middle = (glfw.get_mouse_button(window, glfw.MOUSE_BUTTON_MIDDLE) == glfw.PRESS)
        self.button_right = (glfw.get_mouse_button(window, glfw.MOUSE_BUTTON_RIGHT) == glfw.PRESS)

    def mouse_move(self, window, xpos, ypos):
        dx = xpos - self.lastx
        dy = ypos - self.lasty
        self.lastx = xpos
        self.lasty = ypos

        if not self.button_left and not self.button_middle and not self.button_right:
            return

        width, height = glfw.get_window_size(window)
        mod_shift = (glfw.get_key(window, glfw.KEY_LEFT_SHIFT) == glfw.PRESS or
                     glfw.get_key(window, glfw.KEY_RIGHT_SHIFT) == glfw.PRESS)

        if self.button_right:
            action = mj.mjtMouse.mjMOUSE_MOVE_H if mod_shift else mj.mjtMouse.mjMOUSE_MOVE_V
        elif self.button_left:
            action = mj.mjtMouse.mjMOUSE_ROTATE_H if mod_shift else mj.mjtMouse.mjMOUSE_ROTATE_V
        else:
            action = mj.mjtMouse.mjMOUSE_ZOOM

        mj.mjv_moveCamera(self.model, action, dx / height, dy / height, self.scene, self.cam)

    def scroll(self, window, xoffset, yoffset):
        action = mj.mjtMouse.mjMOUSE_ZOOM
        mj.mjv_moveCamera(self.model, action, 0.0, -0.05 * yoffset, self.scene, self.cam)

    def update_object_position(self):
        if self.body_id is not None:
            scale_factor = 0.001  # Factor de escala para convertir el movimiento del mouse a unidades del mundo
            new_position = np.array([ 
                (mouse_x - 600) * scale_factor,  # Ajustar según el centro de la ventana
                (450 - mouse_y) * scale_factor,  # Ajustar según el centro de la ventana
                0.2  # Mantener la posición en Z constante
            ])

            # Aquí actualizamos la posición del objeto en la simulación
            # Note que estamos usando self.model.geom_pos y no self.data.body_xpos
            self.model.geom_pos[self.body_id] = new_position

    def save_trajectory_to_json(self, file_name="trajectory.json"):
        """
        Guarda el recorrido del objeto en un archivo JSON
        """
        try:
            with open(file_name, 'w') as f:
                json.dump(object_trajectory, f, indent=4)
            print(f"Recorrido guardado en {file_name}")
        except Exception as e:
            print(f"Error al guardar el archivo JSON: {e}")

    def clear_trajectory(self):
        """
        Borra el recorrido guardado en el archivo JSON
        """
        global object_trajectory
        object_trajectory = []
        print("Recorrido borrado.")

    def run(self):
        try:
            while not glfw.window_should_close(self.window):
                mj.mj_step(self.model, self.data)
                mj.mj_forward(self.model, self.data)

                if button_left:
                    self.update_object_position()
                    self.get_position_data()  # Guardar posición en cada paso

                mj.mjv_updateScene(self.model, self.data, self.opt, None, self.cam, mj.mjtCatBit.mjCAT_ALL.value, self.scene)
                mj.mjr_render(mj.MjrRect(0, 0, 1200, 900), self.scene, self.context)

                glfw.swap_buffers(self.window)
                glfw.poll_events()

            self.save_trajectory_to_json()  # Guardamos el recorrido al finalizar
            self.clear_trajectory()  # Limpiamos el recorrido
        except Exception as e:
            print(f"Error en la simulación: {e}")
        finally:
            glfw.terminate()

def main():
    simulation = simulator("Ball entrega copy\\esfera_prueba.xml")
    simulation.run()

if __name__ == "__main__":
    main()
