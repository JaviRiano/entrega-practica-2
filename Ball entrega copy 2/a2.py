import matplotlib.pyplot as plt
import numpy as np

class ObjetoFisico:
    def __init__(self, masa, posicion, velocidad, aceleracion):
        self.masa = masa
        self.posicion = posicion  # Posición a lo largo de la rampa
        self.velocidad = velocidad
        self.aceleracion = aceleracion

    def aplicar_fuerza(self, fuerza):
        """Aplica una fuerza al objeto físico, actualizando la aceleración."""
        if fuerza < 0:
            raise ValueError("La fuerza no puede ser negativa")
        self.aceleracion = fuerza / self.masa

    def mover(self):
        """Calcula el movimiento del objeto con la aceleración y la velocidad."""
        self.velocidad += self.aceleracion
        self.posicion += self.velocidad

class Esfera(ObjetoFisico):
    def __init__(self, masa, posicion, velocidad, aceleracion, radio):
        super().__init__(masa, posicion, velocidad, aceleracion)
        self.radio = radio

class Rampa:
    def __init__(self, angulo_inclinacion, coef_friccion):
        self.angulo_inclinacion = angulo_inclinacion  # En grados
        self.coef_friccion = coef_friccion

    def calcular_fuerza_gravedad(self, masa):
        """Calcula la componente de la fuerza gravitacional en la dirección de la rampa."""
        gravedad = 9.81  # Aceleración de la gravedad (m/s^2)
        angulo_rad = np.radians(self.angulo_inclinacion)  # Convertir ángulo a radianes
        return masa * gravedad * np.sin(angulo_rad)

    def calcular_fuerza_friccion(self, velocidad):
        """Calcula la fuerza de fricción sobre la esfera."""
        return self.coef_friccion * velocidad  # Fuerza de fricción proporcional a la velocidad

class Simulador:
    def __init__(self, esfera, rampa):
        self.esfera = esfera
        self.rampa = rampa
        self.tiempos = []
        self.posiciones = []

    def simular(self, pasos_de_tiempo):
        """Simula el movimiento de la esfera a lo largo de la rampa."""
        for t in range(pasos_de_tiempo):
            # Calculamos las fuerzas que actúan sobre la esfera
            fuerza_gravedad = self.rampa.calcular_fuerza_gravedad(self.esfera.masa)
            fuerza_friccion = self.rampa.calcular_fuerza_friccion(self.esfera.velocidad)

            # La fuerza neta es la diferencia entre la gravedad y la fricción
            fuerza_neta = fuerza_gravedad - fuerza_friccion

            # Aplicar la fuerza neta a la esfera
            self.esfera.aplicar_fuerza(fuerza_neta)

            # Mover la esfera
            self.esfera.mover()

            # Guardar el tiempo y la posición para graficar
            self.tiempos.append(t)
            self.posiciones.append(self.esfera.posicion)

    def graficar_trayectoria(self):
        """Genera un gráfico de la trayectoria de la esfera a lo largo de la rampa."""
        plt.plot(self.tiempos, self.posiciones, label="Trayectoria de la Esfera")
        plt.xlabel("Tiempo (s)")
        plt.ylabel("Posición (m)")
        plt.title("Movimiento de la Esfera sobre la Rampa")
        plt.legend()
        plt.show()

if __name__ == "__main__":
    # Crear la rampa (30 grados de inclinación, fricción media)
    rampa = Rampa(angulo_inclinacion=30, coef_friccion=0.1)

    # Crear la esfera (masa de 1 kg, posición inicial 0, velocidad inicial 0)
    esfera = Esfera(masa=1, posicion=0, velocidad=0, aceleracion=0, radio=0.1)

    # Crear el simulador con la esfera y la rampa
    simulador = Simulador(esfera, rampa)

    # Simular durante 100 pasos de tiempo
    simulador.simular(pasos_de_tiempo=100)

    # Graficar la trayectoria de la esfera
    simulador.graficar_trayectoria()
