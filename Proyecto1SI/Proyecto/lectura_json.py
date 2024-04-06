import json
from punto_mapa import PuntoMapa

def procesar_archivo_json(archivo):
    puntos = []

    # Abre el archivo JSON
    with open(archivo, "r") as archivo_json:
        # Carga el JSON desde el archivo
        data = json.load(archivo_json)

        # Accede a los elementos del JSON
        tamano_matriz = data["tamano_matriz"]
        filas, columnas = tamano_matriz
        matriz = data["matriz"]

        # Itera sobre los puntos en la matriz
        for i, punto_info in enumerate(matriz):
            nombre, punto_datos = next(iter(punto_info.items()))
            x = i // filas
            y = i % filas
            es_turistico = punto_datos["es_turistico"]
            semaforo = punto_datos["semaforo"]
            tiempo_semaforo = punto_datos["tiempo_semaforo"]
            es_viable = punto_datos["es_viable"]
            direccion = punto_datos["direccion"]
    
            # Crea un objeto PuntoMapa y añádelo a la lista de puntos
            punto_mapa = PuntoMapa(nombre, x, y, es_turistico, semaforo, tiempo_semaforo, es_viable, direccion, puntos)
            puntos.append(punto_mapa)

    return puntos