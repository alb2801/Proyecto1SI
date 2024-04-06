from ruta_mas_corta import buscar_ruta_mas_corta

def TourTrip(puntos, puntos_tour):
    rutas = []
    for i in range(len(puntos_tour) - 1):
        origen = puntos_tour[i]
        destino = puntos_tour[i + 1]
        ruta = buscar_ruta_mas_corta(puntos, origen.nombre, destino.nombre)
        if ruta:
            rutas.append(ruta)
        else:
            print(f"No se encontró una ruta entre {origen.nombre} y {destino.nombre}")
            return None
    return rutas