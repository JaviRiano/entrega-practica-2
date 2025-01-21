import math

class Rampa:
    def __init__(self, inclinacion, longitud, friccion):
        self.inclinacion = inclinacion
        self.longitud = longitud
        self.friccion = friccion

    def calcular_aceleracion(self, masa):
       
        g = 9.81  
        angulo_rad = math.radians(self.inclinacion)
        fuerza_paralela = g * math.sin(angulo_rad)
        fuerza_friccion = g * math.cos(angulo_rad) * self.friccion
        aceleracion = (fuerza_paralela - fuerza_friccion) / masa
        return max(0, aceleracion)  

    def __repr__(self):
        return f"Rampa(inclinacion={self.inclinacion}, longitud={self.longitud}, friccion={self.friccion})"