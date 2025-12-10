# pylint: disable=all
"""
PATRÓN STATE - Estados del Juego
=================================
Permite cambiar el comportamiento del juego según su estado.
"""

from abc import ABC, abstractmethod
import pygame

# =============================================================================
# PATRÓN STATE - INTERFACE
# =============================================================================

class Estado(ABC):
    """
    PATRÓN: STATE
    -------------
    Clase base abstracta para todos los estados del juego.
    Cada estado maneja su propia lógica de entrada, actualización y renderizado.
    """
    
    def __init__(self, gestor_estados):
        self.gestor_estados = gestor_estados
        self.pantalla = gestor_estados.pantalla
    
    @abstractmethod
    def manejar_eventos(self, eventos):
        """Maneja los eventos de entrada en este estado."""
        pass
    
    @abstractmethod
    def actualizar(self):
        """Actualiza la lógica del estado."""
        pass
    
    @abstractmethod
    def dibujar(self):
        """Renderiza el estado en pantalla."""
        pass
    
    def entrar(self):
        """Llamado cuando se entra a este estado."""
        print(f"🎮 [STATE] Entrando a estado: {self.__class__.__name__}")
    
    def salir(self):
        """Llamado cuando se sale de este estado."""
        print(f"🎮 [STATE] Saliendo de estado: {self.__class__.__name__}")


# =============================================================================
# GESTOR DE ESTADOS
# =============================================================================

class GestorEstados:
    """
    Gestiona la transición entre diferentes estados del juego.
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