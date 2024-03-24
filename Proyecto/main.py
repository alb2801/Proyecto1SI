import tkinter as tk
from tkinter import filedialog
from lectura_json import procesar_archivo_json
from ruta_mas_corta import buscar_ruta_mas_corta

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

    if punto_inicial and punto_destino:
        # Llamar a la función buscar_ruta_mas_corta
        ruta_nombres = buscar_ruta_mas_corta(puntos, punto_inicial.nombre, punto_destino.nombre)
        
        if ruta_nombres:
            ruta = [punto for punto in puntos if punto.nombre in ruta_nombres]
            print(f"La ruta más corta desde {punto_inicial.nombre} hasta {punto_destino.nombre} es:")
            for punto in ruta:
                print(f"Punto: {punto.nombre}")
                print("Es turístico:", punto.es_turistico)
                print("Tiene semáforo:", punto.semaforo)
                print("Tiempo del semáforo:", punto.tiempo_semaforo)
                print("Es viable:", punto.es_viable)
                print("Dirección:", punto.direccion)
                print("-------------------------")
        else:
            print(f"No se encontró una ruta desde {punto_inicial.nombre} hasta {punto_destino.nombre}.")

if __name__ == "__main__":
    main()
