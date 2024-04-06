import tkinter as tk
from tkinter import filedialog
from vehiculo import Vehiculo
from lectura_json import procesar_archivo_json
from ruta_mas_corta import buscar_ruta_mas_corta
from ruta_mas_rapida import buscar_ruta_mas_rapida
from menor_consumo import buscar_ruta_menor_consumo
from tour_trip import TourTrip


def crear_mapa(puntos):
    filas = max(punto.y for punto in puntos) + 1
    columnas = max(punto.x for punto in puntos) + 1
    mapa = [[[] for _ in range(columnas)] for _ in range(filas)]

    for punto in puntos:
        mapa[punto.y][punto.x] = punto

    return mapa

def main():
    root = tk.Tk()
    root.withdraw()  # Oculta la ventana principal de Tkinter

    # Abre un cuadro de diálogo para seleccionar un archivo
    archivo = filedialog.askopenfilename(filetypes=[("Archivos JSON", "*.json")])

    # Verifica si se seleccionó un archivo
    if archivo:
        # Procesa el archivo JSON seleccionado
        puntos = procesar_archivo_json(archivo)
        # # Imprime la información de cada punto
        # for punto in puntos:
        #     print(f"Punto: {punto.nombre}")
        #     print("Es turístico:", punto.es_turistico)
        #     print("Tiene semáforo:", punto.semaforo)
        #     print("Tiempo del semáforo:", punto.tiempo_semaforo)
        #     print("Es viable:", punto.es_viable)
        #     print("Dirección:", punto.direccion)
        #     print("-------------------------")
            
    # Crea el mapa a partir de los puntos
    mapa = crear_mapa(puntos)

    # Encuentra el punto inicial y el punto destino
    punto_inicial = next((punto for punto in puntos if punto.nombre == "punto1"), None)
    punto_destino = next((punto for punto in puntos if punto.nombre == "punto15"), None)

    #llamado ruta mas corta, sin semaforos
    # if punto_inicial and punto_destino:
    #     # Llamar a la función buscar_ruta_mas_corta
    #     ruta_nombres = buscar_ruta_mas_corta(puntos, punto_inicial.nombre, punto_destino.nombre)
        
    #     if ruta_nombres:
    #         ruta = [punto for punto in puntos if punto.nombre in ruta_nombres]
    #         print(f"La ruta más corta desde {punto_inicial.nombre} hasta {punto_destino.nombre} es:")
    #         for punto in ruta:
    #             print(f"Punto: {punto.nombre}")
    #             print("Es turístico:", punto.es_turistico)
    #             print("Tiene semáforo:", punto.semaforo)
    #             print("Tiempo del semáforo:", punto.tiempo_semaforo)
    #             print("Es viable:", punto.es_viable)
    #             print("Dirección:", punto.direccion)
    #             print("-------------------------")
    #     else:
    #         print(f"No se encontró una ruta desde {punto_inicial.nombre} hasta {punto_destino.nombre}.")
    
    # Vehículo 1 (alto consumo)
    vehiculo1 = Vehiculo(eficiencia_combustible=8, ubicacion="punto1")

    # Vehículo 2 (consumo promedio)
    vehiculo2 = Vehiculo(eficiencia_combustible=12, ubicacion="punto10")

    # Vehículo 3 (bajo consumo)
    vehiculo3 = Vehiculo(eficiencia_combustible=16, ubicacion="punto12")
    """
    if punto_inicial and punto_destino:
        # Llamar a la función buscar_ruta_menor_consumo
        ruta_nombres, consumo_combustible = buscar_ruta_menor_consumo(puntos, punto_inicial.nombre, punto_destino.nombre, vehiculo1.eficiencia_combustible)
    
        if ruta_nombres:
            ruta = [punto for punto in puntos if punto.nombre in ruta_nombres]
            print(f"La ruta más corta desde {punto_inicial.nombre} hasta {punto_destino.nombre} es:")
            print(f"Ruta: {' -> '.join(ruta_nombres)}")
            print(f"Consumo de combustible: {consumo_combustible} litros")
            for punto in ruta:
                print(f"Punto: {punto.nombre}")
                print("Es turístico:", punto.es_turistico)
                print("Es viable:", punto.es_viable)
                print("Dirección:", punto.direccion)
                print("-------------------------")
        else:
            print(f"No se encontró una ruta desde {punto_inicial.nombre} hasta {punto_destino.nombre}.")"""

    if punto_inicial and punto_destino:
        # Llamar a la función buscar_ruta_ás rapida
        ruta_nom, tiempo = buscar_ruta_mas_rapida(puntos, punto_inicial.nombre, punto_destino.nombre)
    
        if ruta_nom:
            ruta = [punto for punto in puntos if punto.nombre in ruta_nom]
            print(f"La ruta más rápida desde {punto_inicial.nombre} hasta {punto_destino.nombre} es:")
            print(f"Ruta: {' -> '.join(ruta_nom)}")
            print(f"Tiempo requerido: {tiempo} segundos")
            for punto in ruta:
                print(f"Punto: {punto.nombre}")
                print("Es semaforo:", punto.semaforo)
                print("Tiempo:", punto.tiempo_semaforo)
                print("-------------------------")
        else:
            print(f"No se encontró una ruta desde {punto_inicial.nombre} hasta {punto_destino.nombre}.")

    puntos_turisticos = [punto for punto in puntos if punto.es_turistico]

    puntos_turisticos = [punto for fila in mapa for punto in fila if punto.es_turistico]

    for i in puntos_turisticos:
        print(f"Punto: {i.nombre}")

    rutas_tour = TourTrip(puntos, puntos_turisticos)
    print("La ruta del tour es: ")
    if rutas_tour:
        for ruta in rutas_tour:
            cont=1
            for ruta_p in ruta:
                if cont!=0:
                    print(ruta_p," -> ", end="")
                cont=cont+1
            cont=0

    else:
        print("No se pudo realizar el recorrido completo")

if __name__ == "__main__":
    main()
    