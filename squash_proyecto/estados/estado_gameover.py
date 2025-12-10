# pylint: disable=all
"""
Estado Game Over
================
"""

import pygame
from estados.estado_base import Estado

class EstadoGameOver(Estado):
    """
    Estado de Game Over.
    Muestra estadísticas finales y opciones.
    """
    
    def __init__(self, gestor_estados, estado_jugando):
        super().__init__(gestor_estados)
        
        # Guardar datos del juego
        self.puntaje_final = estado_jugando.puntaje
        self.nivel_final = estado_jugando.nivel
        self.combo_maximo = estado_jugando.observador_puntaje.mejor_combo
        self.precision = estado_jugando.observador_estadisticas.calcular_precision()
        self.golpes_totales = estado_jugando.observador_estadisticas.golpes_totales
        
        # Fuentes
        self.fuente_titulo = pygame.font.Font(None, 80)
        self.fuente_stat = pygame.font.Font(None, 36)
        self.fuente_opcion = pygame.font.Font(None, 40)
        
        # Opciones
        self.opciones = [
            "Jugar de Nuevo",
            "Volver al Menú",
            "Salir"
        ]
        
        self.opcion_seleccionada = 0
        
        # Colores
        self.color_fondo = (20, 20, 30)
        self.color_titulo = (255, 50, 50)
        self.color_stat = (200, 200, 200)
        self.color_destaque = (0, 255, 200)
        self.color_opcion = (200, 200, 200)
        self.color_seleccionado = (255, 255, 0)
    
    def manejar_eventos(self, eventos):
        """Maneja eventos del menú de game over."""
        for evento in eventos:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP or evento.key == pygame.K_w:
                    self.opcion_seleccionada = max(0, self.opcion_seleccionada - 1)
                
                elif evento.key == pygame.K_DOWN or evento.key == pygame.K_s:
                    self.opcion_seleccionada = min(len(self.opciones) - 1, self.opcion_seleccionada + 1)
                
                elif evento.key == pygame.K_RETURN or evento.key == pygame.K_SPACE:
                    self.ejecutar_opcion()
    
    def actualizar(self):
        """No hay actualizaciones en game over."""
        pass
    
    def dibujar(self):
        """Dibuja la pantalla de game over."""
        self.pantalla.fill(self.color_fondo)
        
        # Título
        texto_titulo = self.fuente_titulo.render("GAME OVER", True, self.color_titulo)
        rect_titulo = texto_titulo.get_rect(center=(500, 80))
        self.pantalla.blit(texto_titulo, rect_titulo)
        
        # Estadísticas
        y_stats = 170
        espaciado_stats = 45
        
        stats = [
            ("Puntaje Final:", f"{self.puntaje_final:,}", True),
            ("Nivel Alcanzado:", f"{self.nivel_final}", False),
            ("Mejor Combo:", f"x{self.combo_maximo}", False),
            ("Golpes Totales:", f"{self.golpes_totales}", False),
            ("Precisión:", f"{self.precision:.1f}%", False)
        ]
        
        for i, (etiqueta, valor, destacado) in enumerate(stats):
            color_valor = self.color_destaque if destacado else self.color_stat
            
            texto_etiqueta = self.fuente_stat.render(etiqueta, True, self.color_stat)
            texto_valor = self.fuente_stat.render(valor, True, color_valor)
            
            y_pos = y_stats + i * espaciado_stats
            
            self.pantalla.blit(texto_etiqueta, (250, y_pos))
            self.pantalla.blit(texto_valor, (550, y_pos))
        
        # Mensaje según rendimiento
        mensaje = self.obtener_mensaje_rendimiento()
        texto_mensaje = self.fuente_stat.render(mensaje, True, (150, 150, 255))
        rect_mensaje = texto_mensaje.get_rect(center=(500, y_stats + len(stats) * espaciado_stats + 30))
        self.pantalla.blit(texto_mensaje, rect_mensaje)
        
        # Opciones
        y_opciones = 480
        espaciado_opciones = 60
        
        for i, opcion in enumerate(self.opciones):
            color = self.color_seleccionado if i == self.opcion_seleccionada else self.color_opcion
            
            texto_opcion = self.fuente_opcion.render(opcion, True, color)
            rect_opcion = texto_opcion.get_rect(center=(500, y_opciones + i * espaciado_opciones))
            self.pantalla.blit(texto_opcion, rect_opcion)
        
        
        
        
    def obtener_mensaje_rendimiento(self):
        """Retorna un mensaje según el rendimiento del jugador."""
        if self.puntaje_final >= 1000:
            return "🏆 ¡Eres un maestro del Squash!"
        elif self.puntaje_final >= 500:
            return "⭐ ¡Excelente partida!"
        elif self.puntaje_final >= 200:
            return "👍 ¡Buen trabajo!"
        else:
            return "💪 ¡Sigue practicando!"
    
    def ejecutar_opcion(self):
        """Ejecuta la opción seleccionada."""
        if self.opcion_seleccionada == 0:
            # Jugar de nuevo - volver al menú para seleccionar dificultad
            from estados.estado_menu import EstadoMenu
            self.gestor_estados.cambiar_estado(EstadoMenu(self.gestor_estados))

        elif self.opcion_seleccionada == 1:
            # Volver al menú
            from estados.estado_menu import EstadoMenu
            self.gestor_estados.cambiar_estado(EstadoMenu(self.gestor_estados))

        elif self.opcion_seleccionada == 2:
            # Salir del juego
            import sys
            pygame.quit()
            sys.exit()
