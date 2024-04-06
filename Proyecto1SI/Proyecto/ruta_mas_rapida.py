from collections import deque, namedtuple
import heapq

def buscar_ruta_mas_rapida(puntos, inicio, destino):
    # Crear un conjunto para rastrear los nodos visitados
    visitados = set()

    # Crear una cola de prioridad para el algoritmo
    cola = []
    heapq.heappush(cola, (0, inicio, [inicio]))  # (tiempo_acumulado, nodo_actual, ruta)

    # Encontrar el objeto PuntoMapa correspondiente al destino
    punto_destino = next((punto for punto in puntos if punto.nombre == destino), None)

    while cola:
        tiempo_acumulado, nodo_actual, ruta = heapq.heappop(cola)

        # Encontrar el objeto PuntoMapa correspondiente al nodo_actual
        punto_actual = next((punto for punto in puntos if punto.nombre == nodo_actual), None)

        # Si se llegó al destino, devolver la ruta y el tiempo
        if punto_actual.nombre == punto_destino.nombre:
            return ruta, tiempo_acumulado

        # Marcar el nodo actual como visitado
        visitados.add(nodo_actual)

        # Obtener los movimientos posibles desde el nodo actual
        movimientos_posibles = punto_actual.movimientos_posible()

        # Explorar los movimientos posibles
        for dx, dy in movimientos_posibles:
            nuevo_x = punto_actual.x + dx
            nuevo_y = punto_actual.y + dy
            nuevo_nodo = next((punto.nombre for punto in puntos if punto.x == nuevo_x and punto.y == nuevo_y and punto.es_viable), None)

            # Si el nuevo nodo es válido y no ha sido visitado
            if nuevo_nodo and nuevo_nodo not in visitados:
                if punto_actual.semaforo:
                    nuevo_tiempo = tiempo_acumulado + punto_actual.tiempo_semaforo
                    nueva_ruta = ruta + [nuevo_nodo]
                    heapq.heappush(cola, (nuevo_tiempo, nuevo_nodo, nueva_ruta))
                else:
                    nuevo_tiempo = tiempo_acumulado + 0
                    nueva_ruta = ruta + [nuevo_nodo]
                    heapq.heappush(cola, (nuevo_tiempo, nuevo_nodo, nueva_ruta))

    # Si no se encontró una ruta, devolver None
    return None