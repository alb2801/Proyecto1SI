from ruta_mas_corta import buscar_ruta_mas_corta

def TourTrip(puntos, puntos_tour, punto_inicial):
    rutas = []
    for i in range(len(puntos_tour)):
        origen = puntos_tour[i]
        destino = punto_inicial if i == len(puntos_tour) - 1 else puntos_tour[i + 1]
        ruta = buscar_ruta_mas_corta(puntos, origen.nombre, destino.nombre)
        if ruta:
            rutas.append(ruta)
        else:
            print(f"No se encontró una ruta entre {origen.nombre} y {destino.nombre}")
            return None
    
    # Agregar la ruta de regreso al punto inicial al final
    ruta_vuelta = buscar_ruta_mas_corta(puntos, puntos_tour[-1].nombre, punto_inicial.nombre)
    if ruta_vuelta:
        rutas.append(ruta_vuelta)
    else:
        print(f"No se encontró una ruta de regreso al punto inicial desde {puntos_tour[-1].nombre}")
        return None
    
    return rutas
