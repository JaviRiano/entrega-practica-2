import mujoco as mj
from mujoco.glfw import glfw
import numpy as np

class simulator:    
    def __init__(self, path):
        # Inicialización de parámetros de la simulación
        self.button_left=False
        self.button_middle=False
        self.button_right=False

        self.lastx=0
        self.lasty=0
        
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
        glfw.swap_interval(1)
        
        # Cargar el modelo de MuJoCo
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

        # Obtener el ID del objeto
        self.object_name = 'sphere'
        self.object_id = mj.mj_name2id(self.model, mj.mjtObj.mjOBJ_GEOM, self.object_name)

    # Método para manejar los eventos de teclado
    def keyboard(self, window, key, scancode, act, mods):
        if act == glfw.PRESS and key == glfw.KEY_BACKSPACE:
            mj.mj_resetData(self.model, self.data)
            mj.mj_forward(self.model, self.data)
        for i in range(len(self.initial_joint_angles)):
            self.data.qpos[i] = self.initial_joint_angles[i]
        mj.mj_forward(self.model, self.data)

    # Método para manejar los eventos del mouse
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

        mj.mjv_moveCamera(self.model, action, dx/height, dy/height, self.scene, self.cam)

    def scroll(self, window, xoffset, yoffset):
        action = mj.mjtMouse.mjMOUSE_ZOOM
        mj.mjv_moveCamera(self.model, action, 0.0, -0.05 * yoffset, self.scene, self.cam)

    # Método para actualizar la posición del objeto
    def update_object_position(self, mouse_x, mouse_y):
        # Precondición: mouse_x y mouse_y deben estar dentro de un rango válido
        assert -1 <= mouse_x <= 1, "Valor fuera de rango para mouse_x"
        assert -1 <= mouse_y <= 1, "Valor fuera de rango para mouse_y"

        if self.object_id is not None:
            scale_factor = 0.001
            new_position = np.array([
                (mouse_x - 600) * scale_factor,
                (450 - mouse_y) * scale_factor,
                0.2
            ])
            
            # Postcondición: La posición del objeto debe haberse actualizado
            self.model.geom_pos[self.object_id] = new_position
            assert np.allclose(self.model.geom_pos[self.object_id], new_position), "La posición no se actualizó correctamente"

    # Método para obtener las posiciones X, Y del objeto
    def get_position(self):
        # Retorna la posición X, Y del objeto en el espacio
        position = self.model.geom_pos[self.object_id]
        return position[0], position[1]

    def run(self):
        while not glfw.window_should_close(self.window):
            mj.mj_step(self.model, self.data)
            mj.mj_forward(self.model, self.data)
            
            if self.button_left:
                self.update_object_position(0.5, 0.5)  # Ejemplo de actualización de la posición
            
            # Actualizar la escena
            mj.mjv_updateScene(self.model, self.data, self.opt, None, self.cam, mj.mjtCatBit.mjCAT_ALL.value, self.scene)
            mj.mjr_render(mj.MjrRect(0, 0, 1200, 900), self.scene, self.context)
            
            glfw.swap_buffers(self.window)
            glfw.poll_events()

        glfw.terminate()
def main():
    simulation=simulator("Ball entrega copy\\esfera_prueba.xml")
    simulation.run()

if __name__ == "__main__":
    main()    
        