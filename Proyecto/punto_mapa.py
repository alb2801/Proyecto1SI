class PuntoMapa:
    def __init__(self, nombre, x, y, es_turistico, semaforo, tiempo_semaforo, es_viable, direccion, puntos):
        self.nombre = nombre
        self.x = x
        self.y = y
        self.es_turistico = es_turistico
        self.semaforo = semaforo
        self.tiempo_semaforo = tiempo_semaforo
        self.es_viable = es_viable
        self.direccion = direccion
        self.puntos = puntos

    def movimientos_posible(self):
        movimientos = []
        direcciones = {
            'norte': (-1, 0),
            'sur': (1, 0),
            'este': (0, 1),
            'oeste': (0, -1)
        }
    
        for direccion in self.direccion:
            direccion_normalizada = direccion.lower()
            if direccion_normalizada in direcciones:
                dx, dy = direcciones[direccion_normalizada]
                nuevo_x = self.x + dx
                nuevo_y = self.y + dy
                nuevo_punto = next((punto for punto in self.puntos if punto.x == nuevo_x and punto.y == nuevo_y and punto.es_viable), None)
                if nuevo_punto:
                    movimientos.append((dx, dy))
            else:
                # La dirección no es válida
                pass
    
        return movimientos
    
    def generar_flechas_movimientos(self):
        movimientos = self.movimientos_posible()
        flechas = []
        for dx, dy in movimientos:
            inicio_x = self.x
            inicio_y = self.y
            fin_x = self.x + dx * 0.3  # Ajusta la longitud de la flecha multiplicando por un factor
            fin_y = self.y + dy * 0.3  # Ajusta la longitud de la flecha multiplicando por un factor
            flechas.append(((inicio_x, inicio_y), (fin_x, fin_y)))
        return flechas