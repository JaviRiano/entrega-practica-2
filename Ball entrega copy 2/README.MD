En este apartado se explicara todos los apartados del codigo en orden
-Balon: El código define una clase Ball para representar una esfera con propiedades físicas y movimiento:

Atributos:

radio, masa, color: Propiedades básicas.
posicion: Coordenadas iniciales (por defecto (0, 0)).
velocidad: Velocidad inicial (0).
Método actualizar_posicion:

Calcula la nueva velocidad y posición basándose en la aceleración y el tiempo transcurrido

Método __repr__:

Devuelve una representación en texto de la esfera para impresión o depuración.

-biblioteca:
Este código ejecuta una simulación física básica usando las clases Ball, Rampa, y Simulacion
Escenario:

Se define un escenario (escenario_1) en un diccionario con configuraciones de esferas (radio, masa, color) y rampas (inclinación, longitud, fricción).
Creación de Objetos:

Se crean objetos Ball y Rampa basados en las configuraciones del escenario.
Simulación:

Se instancia la clase Simulacion con las esferas y rampas.
El método correr simula el movimiento de las esferas durante 5 segundos con intervalos de 0.1 segundos.

-Interfaz gráfica: Este código implementa una interfaz gráfica para cargar configuraciones y ejecutar una simulación. Está dividido en las siguientes partes:

Cargar Configuración:

El botón "Cargar Configuración" permite al usuario seleccionar un archivo JSON desde el sistema de archivos.
El archivo se lee y su contenido se guarda en una variable global config_data.
Se muestra un mensaje de estado indicando si la carga fue exitosa o fallida.
Ejecutar Simulación:

El botón "Iniciar Simulación" utiliza los datos de configuración cargados (o un archivo XML predeterminado si no se especifica uno).
Llama al método simulator.run() para iniciar la simulación.
Muestra un mensaje de éxito o un error en caso de fallos.
Interfaz Gráfica:

Usa CustomTkinter para crear la ventana.
Contiene dos botones:
Cargar Configuración: Carga un archivo JSON.
Iniciar Simulación: Ejecuta la simulación con los datos cargados.
Un mensaje de estado dinámico indica el progreso o los errores.

-Prueba: Este código implementa un simulador utilizando MuJoCo para visualizar y mover un objeto (en este caso, una esfera) dentro de una escena. Los eventos de la interfaz gráfica, como los movimientos del mouse y las teclas del teclado, son manejados para interactuar con la simulación:

Inicialización de MuJoCo y GLFW:
Se crea una ventana utilizando GLFW para manejar la interacción del usuario.
Se carga un modelo MuJoCo desde un archivo XML y se inicializa la escena.
Eventos de Entrada:
Teclado: Al presionar la tecla BACKSPACE, se reinicia la simulación y los objetos vuelven a su posición inicial.
Mouse:
Se detectan las pulsaciones de los botones del mouse (izquierdo, derecho y medio) y el movimiento del mouse.
El movimiento del mouse afecta la cámara, permitiendo rotar, mover y hacer zoom en la escena 3D.
Cuando el botón izquierdo del mouse está presionado, se actualiza la posición de la esfera según el movimiento del mouse.
Simulación:
La simulación se actualiza en un bucle. En cada paso del bucle:
Se realiza un paso de simulación con mj_step y mj_forward.
Si el botón izquierdo está presionado, se actualiza la posición del objeto (sphere) con el movimiento del mouse.
Se renderiza la escena y se muestran los cambios en la ventana.
Main Loop:
Se mantiene la ventana abierta y actualiza la escena hasta que se cierra.

-Rampa:
Este código define una clase Rampa que simula una rampa inclinada con fricción. La clase tiene métodos para calcular la aceleración de un objeto que se desliza por la rampa, teniendo en cuenta la inclinación de la rampa, la fricción y la masa del objeto.

Atributos:

inclinacion: Ángulo de inclinación de la rampa.
longitud: Longitud de la rampa.
friccion: Coeficiente de fricción entre el objeto y la rampa.
Métodos:

calcular_aceleracion(masa): Calcula la aceleración del objeto en la rampa usando la fórmula de la física:
La aceleración se determina a partir de la fuerza gravitacional que actúa en la dirección de la rampa y la fuerza de fricción que se opone al movimiento. La aceleración final es la diferencia entre estas dos fuerzas dividida por la masa del objeto.
El valor de la aceleración se limita a no ser negativo, lo que garantiza que no haya una aceleración "decreciente".
Representación:

El método __repr__ devuelve una representación en cadena de la rampa con sus parámetros.

-Simulacion:
Este código define una clase Simulacion que gestiona y ejecuta una simulación física de un balón (esfera) moviéndose por diferentes rampas.

Atributos:

balon: Lista de objetos Ball (balones o esferas) a simular.
rampas: Lista de objetos Rampa por los cuales los balones se deslizan.
tiempo: Tiempo acumulado de la simulación.
Métodos:

correr(delta_t, duracion): Ejecuta la simulación durante un período de tiempo determinado (duracion), con pasos de tiempo (delta_t). Calcula el número de pasos y llama al método actualizar() en cada paso.

actualizar(delta_t): Para cada balón y cada rampa, calcula la aceleración del balón usando la rampa y actualiza la posición del balón con la aceleración calculada. Este proceso simula el movimiento del balón por la rampa.

Representación:

El método __repr__ devuelve una representación en cadena de la simulación, mostrando los balones y rampas involucrados.