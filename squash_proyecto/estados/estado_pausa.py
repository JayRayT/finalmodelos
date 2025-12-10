# pylint: disable=all
"""
Estado de Pausa
===============
"""

import pygame
from estados import Estado

class EstadoPausa(Estado):
    """
    Estado de pausa del juego.
    Se superpone sobre el estado de juego.
    """
    
    def __init__(self, gestor_estados):
        super().__init__(gestor_estados)
        
        # Fuentes
        self.fuente_titulo = pygame.font.Font(None, 72)
        self.fuente_opcion = pygame.font.Font(None, 40)
        
        # Opciones
        self.opciones = [
            "Continuar",
            "Volver al Menú",
            "Salir"
        ]
        
        self.opcion_seleccionada = 0
        
        # Colores
        self.color_overlay = (0, 0, 0, 180)  # Fondo semi-transparente
        self.color_titulo = (255, 255, 255)
        self.color_opcion = (200, 200, 200)
        self.color_seleccionado = (255, 255, 0)
    
    def manejar_eventos(self, eventos):
        """Maneja eventos del menú de pausa."""
        for evento in eventos:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP or evento.key == pygame.K_w:
                    self.opcion_seleccionada = max(0, self.opcion_seleccionada - 1)
                
                elif evento.key == pygame.K_DOWN or evento.key == pygame.K_s:
                    self.opcion_seleccionada = min(len(self.opciones) - 1, self.opcion_seleccionada + 1)
                
                elif evento.key == pygame.K_RETURN or evento.key == pygame.K_SPACE:
                    self.ejecutar_opcion()
                
                elif evento.key == pygame.K_p or evento.key == pygame.K_ESCAPE:
                    # Continuar juego
                    self.gestor_estados.desapilar_estado()
    
    def actualizar(self):
        """No hay actualizaciones en pausa."""
        pass
    
    def dibujar(self):
        """Dibuja el menú de pausa sobre el juego."""
        # Crear superficie semi-transparente
        overlay = pygame.Surface((1000, 700))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.pantalla.blit(overlay, (0, 0))
        
        # Título
        texto_titulo = self.fuente_titulo.render("⏸ PAUSA", True, self.color_titulo)
        rect_titulo = texto_titulo.get_rect(center=(500, 200))
        self.pantalla.blit(texto_titulo, rect_titulo)
        
        # Opciones
        y_inicio = 320
        espaciado = 60
        
        for i, opcion in enumerate(self.opciones):
            color = self.color_seleccionado if i == self.opcion_seleccionada else self.color_opcion
            
            texto_opcion = self.fuente_opcion.render(opcion, True, color)
            rect_opcion = texto_opcion.get_rect(center=(500, y_inicio + i * espaciado))
            self.pantalla.blit(texto_opcion, rect_opcion)
    
    def ejecutar_opcion(self):
        """Ejecuta la opción seleccionada."""
        if self.opcion_seleccionada == 0:
            # Continuar
            self.gestor_estados.desapilar_estado()

        elif self.opcion_seleccionada == 1:
            # Volver al menú
            # Limpiar pila de estados
            self.gestor_estados.pila_estados.clear()
            # Cambiar a menú
            from estados.estado_menu import EstadoMenu
            self.gestor_estados.cambiar_estado(EstadoMenu(self.gestor_estados))

        elif self.opcion_seleccionada == 2:
            # Salir del juego
            import sys
            pygame.quit()
            sys.exit()
