import tkinter as tk
from tkinter import filedialog
from lectura_json import procesar_archivo_json
#from ruta_mas_corta import calcular_ruta_mas_corta_astar

def main():
    root = tk.Tk()
    root.withdraw()  # Oculta la ventana principal de Tkinter

    # Abre un cuadro de diálogo para seleccionar un archivo
    archivo = filedialog.askopenfilename(filetypes=[("Archivos JSON", "*.json")])

    # Verifica si se seleccionó un archivo
    if archivo:
        # Procesa el archivo JSON seleccionado
        puntos = procesar_archivo_json(archivo)
        # Imprime la información de cada punto
        for punto in puntos:
            print(f"Punto: {punto.nombre}")
            print("Es turístico:", punto.es_turistico)
            print("Tiene semáforo:", punto.semaforo)
            print("Tiempo del semáforo:", punto.tiempo_semaforo)
            print("Es viable:", punto.es_viable)
            print("Dirección:", punto.direccion)
            print("-------------------------")
            
    #punto_inicial = "punto1"
    #punto_destino = "punto9"
    #ruta = calcular_ruta_mas_corta_astar(punto_inicial, punto_destino, puntos)
    
    #if ruta:
    #    print(f"La ruta más corta desde {punto_inicial} hasta {punto_destino} es: {ruta}")
    #else:
    #    print(f"No se encontró una ruta desde {punto_inicial} hasta {punto_destino}.")
        
    

if __name__ == "__main__":
    main()
