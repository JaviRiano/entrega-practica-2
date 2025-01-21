class Ball:
    def __init__(self, radio, masa, color):
        self.radio = radio
        self.masa = masa
        self.color = color
        self.posicion = (0, 0) 
        self.velocidad = 0  

    def actualizar_posicion(self, aceleracion, tiempo):
        
        self.velocidad += aceleracion * tiempo
        self.posicion = (self.posicion[0] + self.velocidad * tiempo, self.posicion[1])

    def __repr__(self):
        return f"Ball(radio={self.radio}, masa={self.masa}, color='{self.color}')"