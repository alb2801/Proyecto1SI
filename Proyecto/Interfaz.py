import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QFileDialog, QLabel, QLineEdit, QSplitter
from PyQt5.QtCore import QTimer
from PyQt5.QtCore import Qt
import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from vehiculo import Vehiculo
from lectura_json import procesar_archivo_json
from ruta_mas_corta import buscar_ruta_mas_corta
from ruta_mas_rapida import buscar_ruta_mas_rapida
from menor_consumo import buscar_ruta_menor_consumo
from tour_trip import TourTrip

matplotlib.use('Qt5Agg')

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Rutas")
        self.setGeometry(5, 40, 1350, 700)

        # Crear la figura y el canvas
        self.figura = Figure()
        self.canvas = FigureCanvas(self.figura)

        # Crear un widget central
        self.splitter = QSplitter(Qt.Horizontal)
        self.setCentralWidget(self.splitter)

        # Crear los elementos de la interfaz
        self.crear_elementos_interfaz()

        # Lista para almacenar los vehículos creados
        self.vehiculos = []

    def crear_elementos_interfaz(self):
    
        # Crear el área para los botones y otros elementos
        widget_izquierda = QWidget()
        layout_izquierda = QVBoxLayout()
        boton_seleccionar_json = QPushButton("Seleccionar JSON")
        boton_seleccionar_json.clicked.connect(self.seleccionar_json)
        layout_izquierda.addWidget(boton_seleccionar_json)
    
        # Agregar labels y lineedits para ingresar ubicación inicial y destino
        label_ubicacion_inicial = QLabel("Ubicación Inicial:")
        self.lineedit_ubicacion_inicial = QLineEdit()
        label_destino = QLabel("Destino:")
        self.lineedit_destino = QLineEdit()
    
        layout_izquierda.addWidget(label_ubicacion_inicial)
        layout_izquierda.addWidget(self.lineedit_ubicacion_inicial)
        layout_izquierda.addWidget(label_destino)
        layout_izquierda.addWidget(self.lineedit_destino)
    
        # Agregar labels y lineedits para ingresar los vehículos
        label_vehiculo1 = QLabel("Vehículo 1 (Eficiencia Combustible - Ubicación):")
        self.lineedit_vehiculo1 = QLineEdit()
        label_vehiculo2 = QLabel("Vehículo 2 (Eficiencia Combustible - Ubicación):")
        self.lineedit_vehiculo2 = QLineEdit()
        label_vehiculo3 = QLabel("Vehículo 3 (Eficiencia Combustible - Ubicación):")
        self.lineedit_vehiculo3 = QLineEdit()
    
        layout_izquierda.addWidget(label_vehiculo1)
        layout_izquierda.addWidget(self.lineedit_vehiculo1)
        layout_izquierda.addWidget(label_vehiculo2)
        layout_izquierda.addWidget(self.lineedit_vehiculo2)
        layout_izquierda.addWidget(label_vehiculo3)
        layout_izquierda.addWidget(self.lineedit_vehiculo3)
        
        # Agregar el botón "Ingresar Datos"
        boton_ingresar_datos = QPushButton("Ingresar Datos")
        boton_ingresar_datos.clicked.connect(self.ingresar_datos)
        layout_izquierda.addWidget(boton_ingresar_datos)
        cambiar_datos = QPushButton("Cambiar datos")
        cambiar_datos.clicked.connect(self.cambiar_datos)
        layout_izquierda.addWidget(cambiar_datos)
        
        # Crear los botones adicionales
        boton_ruta_mas_corta = QPushButton("Ruta Más Corta")
        boton_ruta_mas_corta.clicked.connect(self.buscar_ruta_mas_corta)
        boton_ruta_mas_rapida = QPushButton("Ruta Más Rápida")
        boton_ruta_mas_rapida.clicked.connect(self.buscar_ruta_mas_rapida)
        boton_ruta_menor_combustible = QPushButton("Ruta Menor Combustible")
        boton_ruta_menor_combustible.clicked.connect(self.mostrar_ruta_menor_combustible)
        boton_tour_trip = QPushButton("Tour Trip")
        boton_tour_trip.clicked.connect(self.tour_trip)
    
        layout_izquierda.addWidget(boton_ruta_mas_corta)
        layout_izquierda.addWidget(boton_ruta_mas_rapida)
        layout_izquierda.addWidget(boton_ruta_menor_combustible)
        layout_izquierda.addWidget(boton_tour_trip)
        
        widget_izquierda.setLayout(layout_izquierda)
    
        # Crear el área para mostrar la gráfica
        widget_derecha = QWidget()
        layout_derecha = QVBoxLayout()
        layout_derecha.addWidget(self.canvas)
        widget_derecha.setLayout(layout_derecha)
        
    
        self.splitter.addWidget(widget_izquierda)
        self.splitter.addWidget(widget_derecha)
        
        self.splitter.setSizes([300, 900])

    def cambiar_datos(self):
        self.lineedit_ubicacion_inicial.setEnabled(True)
        self.lineedit_destino.setEnabled(True)
        self.lineedit_vehiculo1.setEnabled(True)
        self.lineedit_vehiculo2.setEnabled(True)
        self.lineedit_vehiculo3.setEnabled(True)

    def seleccionar_json(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Seleccionar archivo JSON", "", "Archivos JSON (*.json)", options=options)
        if file_name:
            self.puntos = procesar_archivo_json(file_name)
            self.graficar_puntos()

    def graficar_puntos(self):
        if self.figura:
            self.figura.clear()
            ax = self.figura.add_subplot(111)
    
            # Graficar puntos únicos con colores correspondientes
            puntos_unicos = {}
            for punto in self.puntos:
                ubicacion = (punto.x, punto.y)
                if ubicacion not in puntos_unicos:
                    puntos_unicos[ubicacion] = punto
    
            for ubicacion, punto in puntos_unicos.items():
                color = 'g' if punto.es_turistico else ('b' if punto.es_viable else 'r')
                ax.plot(ubicacion[0], ubicacion[1], 's', color=color, markersize=60)
                ax.annotate(punto.nombre, (ubicacion[0], ubicacion[1] - 0.4), fontsize=10, ha='center')
                if punto.semaforo:
                    ax.annotate('Semáforo', (ubicacion[0], ubicacion[1] + 0.3), fontsize=10, ha='center')
            # Añadir flechas de posibles movimientos
            for punto in self.puntos:
                flechas_movimientos = punto.generar_flechas_movimientos()
                for flecha in flechas_movimientos:
                    ax.annotate('', xy=flecha[1], xytext=flecha[0], arrowprops=dict(facecolor='black', arrowstyle='->'))
    
            # Ajustar límites del eje
            ax.set_xlim([-1, max([punto.x for punto in self.puntos]) + 1])
            ax.set_ylim([-1, max([punto.y for punto in self.puntos]) + 1])
    
            # Actualizar canvas
            self.canvas.draw()
            
    def ingresar_datos(self):
        self.lineedit_ubicacion_inicial.setEnabled(False)
        self.lineedit_destino.setEnabled(False)
        self.lineedit_vehiculo1.setEnabled(False)
        self.lineedit_vehiculo2.setEnabled(False)
        self.lineedit_vehiculo3.setEnabled(False)
    
        # Obtener el punto destino
        punto_destino = None
    
        for punto in self.puntos:
            if punto.nombre == self.lineedit_ubicacion_inicial.text():
                punto_destino = punto
    
        if punto_destino:
            rutas = []  # Lista para almacenar las rutas y sus longitudes
    
            # Crear los vehículos a partir de los valores ingresados
            vehiculo1_datos = self.lineedit_vehiculo1.text().split('-')
            eficiencia_combustible1 = int(vehiculo1_datos[0].strip())
            ubicacion1 = vehiculo1_datos[1].strip()
    
            vehiculo2_datos = self.lineedit_vehiculo2.text().split('-')
            eficiencia_combustible2 = int(vehiculo2_datos[0].strip())
            ubicacion2 = vehiculo2_datos[1].strip()
    
            vehiculo3_datos = self.lineedit_vehiculo3.text().split('-')
            eficiencia_combustible3 = int(vehiculo3_datos[0].strip())
            ubicacion3 = vehiculo3_datos[1].strip()
    
            vehiculo1 = Vehiculo(eficiencia_combustible=eficiencia_combustible1, ubicacion=ubicacion1)
            vehiculo2 = Vehiculo(eficiencia_combustible=eficiencia_combustible2, ubicacion=ubicacion2)
            vehiculo3 = Vehiculo(eficiencia_combustible=eficiencia_combustible3, ubicacion=ubicacion3)
    
            self.vehiculos = [vehiculo1, vehiculo2, vehiculo3]
    
            # Buscar la ruta más corta para cada vehículo
            for vehiculo in self.vehiculos:
                puntos_con_nombre = [punto for punto in self.puntos if punto.nombre == vehiculo.ubicacion]
                if puntos_con_nombre:
                    punto_inicial = puntos_con_nombre[0]
                    ruta_nombres = buscar_ruta_mas_corta(self.puntos, punto_inicial.nombre, punto_destino.nombre)
                    if ruta_nombres:
                        ruta = [punto for punto in self.puntos if punto.nombre in ruta_nombres]
                        longitud_ruta = len(ruta) - 1  # Calcular la longitud de la ruta como el número de movimientos
                        rutas.append((vehiculo, longitud_ruta, ruta))
                    else:
                        print(f"No se encontró una ruta desde {vehiculo.ubicacion} hasta {punto_destino.nombre}.")
                else:
                    print(f"No se encontró un punto con la ubicación {vehiculo.ubicacion}.")
    
            # Seleccionar la ruta más corta
            if rutas:
                ruta_mas_corta = min(rutas, key=lambda x: x[1])
                vehiculo_ruta_mas_corta = ruta_mas_corta[0]  # Obtener el vehículo de la ruta más corta
                eficiencia_combustible_vehiculo = vehiculo_ruta_mas_corta.eficiencia_combustible
    
                # Crear un nuevo vehículo con la ubicación actualizada al destino
                nuevo_vehiculo = Vehiculo(eficiencia_combustible=eficiencia_combustible_vehiculo, ubicacion=punto_destino.nombre)
                self.vehiculos.append(nuevo_vehiculo)  # Agregar el nuevo vehículo a la lista
    
                print(f"La ruta más corta es desde {ruta_mas_corta[0].ubicacion} con una longitud de {ruta_mas_corta[1]}")
                print("Detalles de la ruta:")
                for punto in ruta_mas_corta[2]:
                    print(f"Punto: {punto.nombre}")
                    print("Es turístico:", punto.es_turistico)
                    print("Tiene semáforo:", punto.semaforo)
                    print("Tiempo del semáforo:", punto.tiempo_semaforo)
                    print("Es viable:", punto.es_viable)
                    print("Dirección:", punto.direccion)
                    print("-------------------------")
    
                self.graficar_ruta_seleccionada(ruta_mas_corta[2])
            else:
                print("No se encontraron rutas válidas.")
        else:
            print("Debe ingresar una ubicación inicial válida.")
                
            
            
    def buscar_ruta_mas_corta(self):
        punto_inicial = None
        punto_destino = None
    
        for punto in self.puntos:
            if punto.nombre == self.lineedit_ubicacion_inicial.text():
                punto_inicial = punto
            if punto.nombre == self.lineedit_destino.text():
                punto_destino = punto
    
        if punto_inicial and punto_destino:
            ruta_nombres = buscar_ruta_mas_corta(self.puntos, punto_inicial.nombre, punto_destino.nombre)
    
            if ruta_nombres:
                ruta = [punto for punto in self.puntos if punto.nombre in ruta_nombres]
                self.graficar_ruta_seleccionada(ruta, estilo='D', color='gray')
    
                # Imprimir la ruta seleccionada por consola
                print("Ruta seleccionada:")
                for punto in ruta:
                    print(punto.nombre)
    
                # Contar el número de puntos en la ruta y mostrarlo como "coste"
                coste = len(ruta)
                print(f"Coste: {coste}")
    
            else:
                print(f"No se encontró una ruta desde {punto_inicial.nombre} hasta {punto_destino.nombre}.")
        else:
            print("Debe ingresar una ubicación inicial y un destino válidos.")
    
    def mostrar_ruta_menor_combustible(self):
        punto_inicial = None
        punto_destino = None
    
        for punto in self.puntos:
            if punto.nombre == self.lineedit_ubicacion_inicial.text():
                punto_inicial = punto
            if punto.nombre == self.lineedit_destino.text():
                punto_destino = punto
    
        if punto_inicial and punto_destino:
            # Encontrar el nuevo vehículo agregado después de seleccionar la ruta más corta
            nuevo_vehiculo = None
            for vehiculo in self.vehiculos:
                if vehiculo.ubicacion == punto_inicial.nombre:
                    nuevo_vehiculo = vehiculo
                    break
    
            if nuevo_vehiculo:
                # Buscar la ruta de menor consumo para el nuevo vehículo
                ruta_nombres, consumo_combustible = buscar_ruta_menor_consumo(self.puntos, nuevo_vehiculo.ubicacion, punto_destino.nombre, nuevo_vehiculo.eficiencia_combustible)
    
                if ruta_nombres:
                    ruta = [punto for punto in self.puntos if punto.nombre in ruta_nombres]
                    self.graficar_ruta_seleccionada(ruta, estilo='D', color='gray')
                    print("La ruta de menor consumo es:")
                    print(f"Ruta: {' -> '.join(ruta_nombres)}")
                    print(f"Consumo de combustible: {consumo_combustible} litros")
                
                    coste = len(ruta)
                    print(f"Coste: {coste}")                
                else:
                    print(f"No se encontró una ruta desde {nuevo_vehiculo.ubicacion} hasta {punto_destino.nombre}.")
            else:
                print("No se encontró el nuevo vehículo agregado.")
        else:
            print("Debe ingresar una ubicación inicial y un destino válidos.")
  
    def buscar_ruta_mas_rapida(self):
        
        punto_inicial = None
        punto_destino = None
    
        for punto in self.puntos:
            if punto.nombre == self.lineedit_ubicacion_inicial.text():
                punto_inicial = punto
            if punto.nombre == self.lineedit_destino.text():
                punto_destino = punto
    
        if punto_inicial and punto_destino:
            # Llamar a la función buscar_ruta_mas_rapida
            ruta_nom, tiempo = buscar_ruta_mas_rapida(self.puntos, punto_inicial.nombre, punto_destino.nombre)
    
            if ruta_nom:
                ruta = [punto for punto in self.puntos if punto.nombre in ruta_nom]
                print(f"La ruta más rápida desde {punto_inicial.nombre} hasta {punto_destino.nombre} es:")
                print(f"Ruta: {' -> '.join(ruta_nom)}")
                print(f"Tiempo requerido: {tiempo} segundos")
                
                coste = len(ruta)
                print(f"Coste: {coste}")
    
                for punto in ruta:
                    print(f"Punto: {punto.nombre}")
                    print("Es semáforo:", punto.semaforo)
                    print("Tiempo:", punto.tiempo_semaforo)
                    print("-------------------------")
    
                self.graficar_ruta_seleccionada(ruta, estilo='D', color='gray')  # Asteriscos azules
            else:
                print(f"No se encontró una ruta desde {punto_inicial.nombre} hasta {punto_destino.nombre}.")
        else:
            print("Debe ingresar una ubicación inicial y un destino válidos.")      
    
    def tour_trip(self):
        punto_inicial = None
        for punto in self.puntos:
            if punto.nombre == self.lineedit_ubicacion_inicial.text():
                punto_inicial = punto
    
        puntos_turisticos = [punto for punto in self.puntos if punto.es_turistico]
        rutas_tour = TourTrip(self.puntos, puntos_turisticos, punto_inicial)
    
        if rutas_tour:
            self.figura.clear()  # Limpia la figura antes de graficar las rutas
            ax = self.figura.add_subplot(111)
    
            # Graficar los puntos únicos
            puntos_unicos = {}
            for punto in self.puntos:
                ubicacion = (punto.x, punto.y)
                if ubicacion not in puntos_unicos:
                    puntos_unicos[ubicacion] = punto
    
            for ubicacion, punto in puntos_unicos.items():
                color_punto = 'g' if punto.es_turistico else ('b' if punto.es_viable else 'r')
                ax.plot(ubicacion[0], ubicacion[1], 's', color=color_punto, markersize=60)
                ax.annotate(punto.nombre, ubicacion, fontsize=8)
    
            # Graficar todas las rutas seleccionadas
            for ruta in rutas_tour:
                ruta_puntos = [punto for punto in self.puntos if punto.nombre in ruta]
                for punto in ruta_puntos:
                    ax.plot(punto.x, punto.y, 'D', color='gray', markersize=10)
    
            print("La ruta del tour es: ")
            if rutas_tour:
                coste_total = 0  # Inicializar el coste total
                for ruta in rutas_tour:
                    cont = 1
                    for ruta_p in ruta:
                        if cont != 0:
                            print(ruta_p, " -> ", end="")
                        cont = cont + 1
                        coste_total += 1  # Incrementar el coste total por cada punto de la ruta
                    cont = 0
                    print()  # Imprimir una nueva línea después de cada ruta
                print("\nCoste total:", coste_total)  # Imprimir el coste total
            else:
                print("No se pudo realizar el recorrido completo")
    
            # Ajustar los límites del eje
            ax.set_xlim([-1, max([punto.x for punto in self.puntos]) + 1])
            ax.set_ylim([-1, max([punto.y for punto in self.puntos]) + 1])
    
            # Actualizar el canvas
            self.canvas.draw()
            timer = QTimer(self)
            timer.setSingleShot(True)
            timer.timeout.connect(self.graficar_puntos)
            timer.start(5000)
    
        else:
            print("No se pudo realizar el recorrido completo")

        
    def graficar_ruta_seleccionada(self, ruta_seleccionada, estilo='o', color='y'):
        if self.figura:
            self.figura.clear()
            ax = self.figura.add_subplot(111)

            # Graficar los puntos únicos
            puntos_unicos = {}
            for punto in self.puntos:
                ubicacion = (punto.x, punto.y)
                if ubicacion not in puntos_unicos:
                    puntos_unicos[ubicacion] = punto

            for ubicacion, punto in puntos_unicos.items():
                color_punto = 'g' if punto.es_turistico else ('b' if punto.es_viable else 'r')
                ax.plot(ubicacion[0], ubicacion[1], 's', color=color_punto, markersize=60)
                ax.annotate(punto.nombre, ubicacion, fontsize=8)

            # Graficar la ruta seleccionada
            for punto in ruta_seleccionada:
                ax.plot(punto.x, punto.y, estilo, color=color, markersize=10)

            # Ajustar los límites del eje
            ax.set_xlim([-1, max([punto.x for punto in self.puntos]) + 1])
            ax.set_ylim([-1, max([punto.y for punto in self.puntos]) + 1])

            # Actualizar el canvas
            self.canvas.draw()

            # Programar la actualización del gráfico después de 10 segundos
            timer = QTimer(self)
            timer.setSingleShot(True)
            timer.timeout.connect(self.graficar_puntos)
            timer.start(5000)

            
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana_principal = VentanaPrincipal()
    ventana_principal.show()
    sys.exit(app.exec_())
