# pylint: disable=all
"""
Estado del Menú Principal
==========================
"""

import pygame
from estados.estado_base import Estado
from estados.estado_jugando import EstadoJugando
from estrategias.difficultad import *

class EstadoMenu(Estado):
    """
    Estado del menú principal del juego.
    Permite seleccionar dificultad e iniciar el juego.
    """
    
    def __init__(self, gestor_estados):
        super().__init__(gestor_estados)
        
        # Fuentes
        self.fuente_titulo = pygame.font.Font(None, 80)
        self.fuente_opcion = pygame.font.Font(None, 40)
        self.fuente_descripcion = pygame.font.Font(None, 28)
        
        # Opciones del menú
        self.opciones = [
            {"texto": "1. Fácil", "dificultad": "facil", "estrategia": DificultadFacil()},
            {"texto": "2. Normal", "dificultad": "normal", "estrategia": DificultadNormal()},
            {"texto": "3. Difícil", "dificultad": "dificil", "estrategia": DificultadDificil()},
            {"texto": "4. Extrema", "dificultad": "extrema", "estrategia": DificultadExtrema()}
        ]
        
        self.opcion_seleccionada = 1  # Normal por defecto
        
        # Colores
        self.color_fondo = (20, 20, 30)
        self.color_titulo = (0, 255, 200)
        self.color_opcion = (200, 200, 200)
        self.color_seleccionado = (255, 255, 0)
        self.color_descripcion = (150, 150, 255)
    
    def manejar_eventos(self, eventos):
        """Maneja eventos del menú."""
        for evento in eventos:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP or evento.key == pygame.K_w:
                    self.opcion_seleccionada = max(0, self.opcion_seleccionada - 1)
                
                elif evento.key == pygame.K_DOWN or evento.key == pygame.K_s:
                    self.opcion_seleccionada = min(len(self.opciones) - 1, self.opcion_seleccionada + 1)
                
                elif evento.key == pygame.K_RETURN or evento.key == pygame.K_SPACE:
                    self.iniciar_juego()
                
                elif evento.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]:
                    indice = evento.key - pygame.K_1
                    if 0 <= indice < len(self.opciones):
                        self.opcion_seleccionada = indice
                        self.iniciar_juego()
    
    def actualizar(self):
        """Actualiza el menú (no hay mucha lógica aquí)."""
        pass
    
    def dibujar(self):
        """Dibuja el menú en pantalla."""
        self.pantalla.fill(self.color_fondo)
        
        # Título
        texto_titulo = self.fuente_titulo.render("🎮 SQUASH", True, self.color_titulo)
        rect_titulo = texto_titulo.get_rect(center=(500, 100))
        self.pantalla.blit(texto_titulo, rect_titulo)
        
        # Subtítulo
        texto_sub = self.fuente_descripcion.render("Proyecto con Patrones de Diseño", True, (100, 200, 255))
        rect_sub = texto_sub.get_rect(center=(500, 150))
        self.pantalla.blit(texto_sub, rect_sub)
        
        # Instrucciones
        texto_inst = self.fuente_descripcion.render("Selecciona la dificultad:", True, (200, 200, 200))
        rect_inst = texto_inst.get_rect(center=(500, 220))
        self.pantalla.blit(texto_inst, rect_inst)
        
        # Opciones de dificultad
        y_inicio = 280
        espaciado = 80
        
        for i, opcion in enumerate(self.opciones):
            color = self.color_seleccionado if i == self.opcion_seleccionada else self.color_opcion
            
            # Texto de la opción
            texto_opcion = self.fuente_opcion.render(opcion["texto"], True, color)
            rect_opcion = texto_opcion.get_rect(center=(500, y_inicio + i * espaciado))
            self.pantalla.blit(texto_opcion, rect_opcion)
            
            # Descripción de la dificultad
            if i == self.opcion_seleccionada:
                estrategia = opcion["estrategia"]
                descripcion = estrategia.obtener_descripcion()
                texto_desc = self.fuente_descripcion.render(descripcion, True, self.color_descripcion)
                rect_desc = texto_desc.get_rect(center=(500, y_inicio + i * espaciado + 30))
                self.pantalla.blit(texto_desc, rect_desc)
        
        # Controles
        y_controles = 600
        controles = [
            "↑↓ o W/S: Navegar | ENTER/SPACE: Iniciar | ESC: Salir",
            "← →: Mover raqueta | A/S/D/W/Q: Cambiar modos"
        ]
        
        for i, control in enumerate(controles):
            texto = self.fuente_descripcion.render(control, True, (150, 150, 150))
            rect = texto.get_rect(center=(500, y_controles + i * 30))
            self.pantalla.blit(texto, rect)
    
    def iniciar_juego(self):
        """Inicia el juego con la dificultad seleccionada."""
        opcion = self.opciones[self.opcion_seleccionada]
        estrategia = opcion["estrategia"]
        
        print(f"\n🎮 [MENU] Iniciando juego con dificultad: {estrategia.obtener_nombre()}\n")
        
        # Cambiar al estado de juego
        estado_jugando = EstadoJugando(self.gestor_estados, estrategia)
        self.gestor_estados.cambiar_estado(estado_jugando)