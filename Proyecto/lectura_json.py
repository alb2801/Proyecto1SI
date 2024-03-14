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
    matriz = data["matriz"]

    # Itera sobre los puntos en la matriz
    for punto in matriz:
        nombre, punto_info = punto.popitem()
        es_turistico = punto_info["es_turistico"]
        semaforo = punto_info["semaforo"]
        tiempo_semaforo = punto_info["tiempo_semaforo"]
        es_viable = punto_info["es_viable"]
        direccion = punto_info["direccion"]

        # Crea un objeto PuntoMapa y añádelo a la lista de puntos
        puntos.append(PuntoMapa(nombre, es_turistico, semaforo, tiempo_semaforo, es_viable, direccion))

    return puntos
