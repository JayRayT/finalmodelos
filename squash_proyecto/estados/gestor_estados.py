# pylint: disable=all
"""
PATRÓN STATE - Gestor de Estados del Juego
===========================================
"""

import pygame

# =============================================================================
# GESTOR DE ESTADOS (CLASE PRINCIPAL)
# =============================================================================

class GestorEstados:
    """
    Gestiona la transición entre diferentes estados del juego.
    Implementa el patrón State.
    """
    
    def __init__(self, pantalla):
        self.pantalla = pantalla
        self.estado_actual = None
        self.pila_estados = []
    
    def cambiar_estado(self, nuevo_estado):
        """
        Cambia completamente al nuevo estado.
        Elimina el estado anterior.
        """
        if self.estado_actual:
            self.estado_actual.salir()
        
        self.estado_actual = nuevo_estado
        self.estado_actual.entrar()
    
    def apilar_estado(self, nuevo_estado):
        """
        Apila un nuevo estado encima del actual.
        Útil para pausas o menús overlay.
        """
        if self.estado_actual:
            self.pila_estados.append(self.estado_actual)
        
        self.estado_actual = nuevo_estado
        self.estado_actual.entrar()
    
    def desapilar_estado(self):
        """
        Vuelve al estado anterior en la pila.
        """
        if self.pila_estados:
            self.estado_actual.salir()
            self.estado_actual = self.pila_estados.pop()
            print(f"🎮 [STATE] Regresando a: {self.estado_actual.__class__.__name__}")
        else:
            print("⚠️ [STATE] No hay estados en la pila")
    
    def actualizar(self, eventos):
        """Actualiza el estado actual."""
        if self.estado_actual:
            self.estado_actual.manejar_eventos(eventos)
            self.estado_actual.actualizar()
    
    def dibujar(self):
        """Dibuja el estado actual."""
        if self.estado_actual:
            self.estado_actual.dibujar()
    
    def obtener_estado_actual(self):
        """Retorna el estado actual."""
        return self.estado_actual
    
    def limpiar_pila(self):
        """Limpia toda la pila de estados."""
        self.pila_estados.clear()
        print("🧹 [STATE] Pila de estados limpiada")