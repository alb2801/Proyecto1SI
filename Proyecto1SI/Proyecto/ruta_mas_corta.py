from collections import deque

def buscar_ruta_mas_corta(puntos, inicio, destino):
    # Crear un conjunto para rastrear los nodos visitados
    visitados = set()
    

    # Crear una cola para el BFS
    cola = deque([(inicio, [inicio])])
    
    # Encontrar el objeto PuntoMapa correspondiente al destino
    punto_destino = next((punto for punto in puntos if punto.nombre == destino), None)
    
    # Iterar hasta que se encuentre la ruta o se agoten los nodos
    while cola:
        nodo_actual, ruta = cola.popleft()
        

        # Encontrar el objeto PuntoMapa correspondiente al nodo_actual
        punto_actual = next((punto for punto in puntos if punto.nombre == nodo_actual), None)
        
        # Si se llegó al destino, devolver la ruta
        if punto_actual.nombre == punto_destino.nombre:
            return ruta

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
                nueva_ruta = ruta + [nuevo_nodo]
                cola.append((nuevo_nodo, nueva_ruta))

    # Si no se encontró una ruta, devolver None
    return None