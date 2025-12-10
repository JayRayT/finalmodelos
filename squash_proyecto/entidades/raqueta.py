# pylint: disable=all
"""
Entidad Raqueta con soporte para PATRÓN DECORATOR
==================================================
"""

import pygame

# =============================================================================
# PATRÓN DECORATOR - PARA MODOS ESPECIALES
# =============================================================================

def modo_especial(func):
    """
    PATRÓN: DECORATOR
    -----------------
    Decorator que agrega validación y logging al activar modos especiales.
    """
    def wrapper(self, tecla_presionada=True):
        if tecla_presionada:
            resultado = func(self)
            if resultado:
                print(f"🎮 [DECORATOR] Modo activado: {func.__name__}")
            return resultado
        return False
    return wrapper


# =============================================================================
# CLASE RAQUETA
# =============================================================================

class Raqueta:
    """
    Raqueta controlable por el jugador.
    Soporta diferentes modos mediante el patrón Decorator.
    """
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.ancho = 100
        self.alto = 15
        self.velocidad = 8
        self.color = (0, 255, 0)
        self.modo_actual = "Normal"
        
        # Configuraciones de cada modo
        self.modos = {
            "Normal": {
                "color": (0, 255, 0),
                "velocidad": 8,
                "ancho": 100,
                "descripcion": "Modo balanceado"
            },
            "Rápido": {
                "color": (255, 255, 0),
                "velocidad": 12,
                "ancho": 80,
                "descripcion": "Más velocidad, menos ancho"
            },
            "Ancho": {
                "color": (255, 0, 0),
                "velocidad": 6,
                "ancho": 150,
                "descripcion": "Más ancho, menos velocidad"
            },
            "Imantación": {
                "color": (0, 0, 255),
                "velocidad": 8,
                "ancho": 100,
                "descripcion": "Atrae la pelota cuando está cerca"
            },
            "Escudo": {
                "color": (255, 0, 255),
                "velocidad": 7,
                "ancho": 120,
                "descripcion": "Rebota la pelota más fuerte"
            }
        }
    
    def cambiar_modo(self, nuevo_modo):
        """Cambia el modo de la raqueta."""
        if nuevo_modo in self.modos:
            self.modo_actual = nuevo_modo
            config = self.modos[nuevo_modo]
            self.color = config["color"]
            self.velocidad = config["velocidad"]
            self.ancho = config["ancho"]
            return True
        return False
    
    # Métodos decorados para activar modos
    
    @modo_especial
    def activar_modo_rapido(self):
        """Activa el modo rápido."""
        return self.cambiar_modo("Rápido")
    
    @modo_especial
    def activar_modo_ancho(self):
        """Activa el modo ancho."""
        return self.cambiar_modo("Ancho")
    
    @modo_especial
    def activar_modo_imantacion(self):
        """Activa el modo imantación."""
        return self.cambiar_modo("Imantación")
    
    @modo_especial
    def activar_modo_normal(self):
        """Activa el modo normal."""
        return self.cambiar_modo("Normal")
    
    @modo_especial
    def activar_modo_escudo(self):
        """Activa el modo escudo."""
        return self.cambiar_modo("Escudo")
    
    def mover(self, teclas_presionadas):
        """Mueve la raqueta según las teclas presionadas."""
        if teclas_presionadas[pygame.K_LEFT] and self.x > 0:
            self.x -= self.velocidad
        if teclas_presionadas[pygame.K_RIGHT] and self.x < 1000 - self.ancho:
            self.x += self.velocidad
    
    def aplicar_imantacion(self, pelota):
        """
        Aplica efecto de imantación si el modo está activo.
        Atrae la pelota hacia el centro de la raqueta.
        """
        if self.modo_actual == "Imantación" and pelota and pelota.activa:
            distancia_x = abs(pelota.x - (self.x + self.ancho / 2))
            
            # Solo aplica si la pelota está cerca
            if distancia_x < 150 and pelota.y > 300:
                # Fuerza de atracción hacia el centro
                fuerza = (pelota.x - (self.x + self.ancho / 2)) * 0.05
                pelota.velocidad_x -= fuerza
                return True
        
        return False
    
    def dibujar(self, superficie):
        """Dibuja la raqueta en la superficie."""
        pygame.draw.rect(superficie, self.color, (self.x, self.y, self.ancho, self.alto))
        
        # Efecto visual para modo escudo
        if self.modo_actual == "Escudo":
            pygame.draw.rect(superficie, (255, 255, 255), 
                           (self.x - 2, self.y - 2, self.ancho + 4, self.alto + 4), 2)
    
    def obtener_info_modo(self):
        """Retorna información del modo actual."""
        return self.modos.get(self.modo_actual, {})