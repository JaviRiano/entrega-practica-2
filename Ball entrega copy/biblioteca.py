from balon import Ball
from rampa import Rampa
from simulacion import Simulacion

escenarios = {
    "escenario_1": {
        "esferas": [
            {"radio": 0.05, "color": "rojo", "masa": 0.1},
            {"radio": 0.07, "color": "azul", "masa": 0.15},
        ],
        "rampas": [
            {"inclinacion": 30, "longitud": 1.5, "friccion": 0.2},
            {"inclinacion": 45, "longitud": 2.0, "friccion": 0.1},
        ],
    }
}


config = escenarios["escenario_1"]


esferas = [Ball(**e) for e in config["esferas"]]
rampas = [Rampa(**r) for r in config["rampas"]]


simulacion = Simulacion(esferas, rampas)
print(simulacion)

simulacion.correr(delta_t=0.1, duracion=5.0)
print("Simulación terminada.")