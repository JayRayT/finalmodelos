"""
PATRÓN FACTORY METHOD - Creación de Pelotas
============================================
"""

import pygame
import random

class Pelota:
    """Clase base para pelotas."""
    
    def __init__(self, x, y, velocidad_x, velocidad_y):
        self.x = x
        self.y = y
        self.velocidad_x = velocidad_x
        self.velocidad_y = velocidad_y
        self.radio = 10
        self.color = (255, 255, 255)
        self.activa = True
        self.tipo = "Normal"
        self.puntos_bonus = 0
    
    def mover(self):
        self.x += self.velocidad_x
        self.y += self.velocidad_y
        
        # Rebotes en bordes
        if self.x <= 0 or self.x >= 1000:
            self.velocidad_x = -self.velocidad_x
        
        if self.y <= 0:
            self.velocidad_y = -self.velocidad_y
        
        # Verificar si se perdió la pelota
        if self.y >= 700:
            self.activa = False
    
    def verificar_colision(self, raqueta):
        if (self.x + self.radio > raqueta.x and 
            self.x - self.radio < raqueta.x + raqueta.ancho and
            self.y + self.radio > raqueta.y and 
            self.y - self.radio < raqueta.y + raqueta.alto):
            
            self.velocidad_y = -abs(self.velocidad_y)
            
            # Ajustar dirección según dónde golpeó
            centro_raqueta = raqueta.x + raqueta.ancho / 2
            diferencia = self.x - centro_raqueta
            self.velocidad_x = diferencia * 0.1
            
            return True
        return False
    
    def efecto_especial(self, juego):
        """Efecto especial (sobrescribir en clases hijas)."""
        pass
    
    def dibujar(self, superficie):
        pygame.draw.circle(superficie, self.color, (int(self.x), int(self.y)), self.radio)


class FabricaPelotas:
    """
    PATRÓN: FACTORY METHOD
    ----------------------
    Crea diferentes tipos de pelotas.
    """
    
    @staticmethod
    def crear_pelota_normal(nivel):
        """Crea una pelota normal."""
        pelota = Pelota(500, 350, 5, -5)
        pelota.color = (255, 255, 255)
        pelota.tipo = "Normal"
        pelota.puntos_bonus = 0
        return pelota
    
    @staticmethod
    def crear_pelota_rapida(nivel):
        """Crea una pelota rápida."""
        pelota = Pelota(500, 350, 7 * (1 + 0.1 * nivel), -7 * (1 + 0.1 * nivel))
        pelota.color = (255, 100, 100)
        pelota.tipo = "Rápida"
        pelota.puntos_bonus = 10
        return pelota
    
    @staticmethod
    def crear_pelota_lenta(nivel):
        """Crea una pelota lenta (da más tiempo)."""
        pelota = Pelota(500, 350, 3, -3)
        pelota.color = (100, 200, 255)
        pelota.tipo = "Lenta"
        pelota.puntos_bonus = 5
        
        def efecto_lento(juego):
            juego.raqueta.velocidad *= 1.5
        
        pelota.efecto_especial = efecto_lento
        return pelota
    
    @staticmethod
    def crear_pelota_puntos_dobles(nivel):
        """Crea una pelota que activa multiplicador de puntos."""
        pelota = Pelota(500, 350, 5, -5)
        pelota.color = (255, 255, 0)
        pelota.tipo = "Puntos Dobles"
        pelota.puntos_bonus = 20
        
        def efecto_doble(juego):
            juego.activar_multiplicador(5)
        
        pelota.efecto_especial = efecto_doble
        return pelota
    
    @staticmethod
    def crear_pelota_vida_extra(nivel):
        """Crea una pelota que otorga vida extra."""
        pelota = Pelota(500, 350, 4, -4)
        pelota.color = (0, 255, 0)
        pelota.tipo = "Vida Extra"
        pelota.puntos_bonus = 15
        
        def efecto_vida(juego):
            juego.vidas += 1
        
        pelota.efecto_especial = efecto_vida
        return pelota
    
    @staticmethod
    def crear_pelota_aleatoria(nivel):
        """
        Crea una pelota aleatoria según la probabilidad.
        Usa la estrategia de dificultad para determinar probabilidades.
        """
        # Por defecto, usar distribución normal
        tipos = ["normal", "rapida", "lenta", "puntos_dobles", "vida_extra"]
        pesos = [40, 20, 15, 15, 10]  # Pesos base
        
        # Ajustar según nivel
        for i in range(nivel - 1):
            if i < len(pesos) - 1:
                pesos[i] -= 5
                pesos[i + 1] += 5
        
        tipo = random.choices(tipos, weights=pesos)[0]
        
        if tipo == "normal":
            return FabricaPelotas.crear_pelota_normal(nivel)
        elif tipo == "rapida":
            return FabricaPelotas.crear_pelota_rapida(nivel)
        elif tipo == "lenta":
            return FabricaPelotas.crear_pelota_lenta(nivel)
        elif tipo == "puntos_dobles":
            return FabricaPelotas.crear_pelota_puntos_dobles(nivel)
        elif tipo == "vida_extra":
            return FabricaPelotas.crear_pelota_vida_extra(nivel)
        
        return FabricaPelotas.crear_pelota_normal(nivel)