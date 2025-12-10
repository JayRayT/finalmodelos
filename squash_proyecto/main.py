# pylint: disable=all
"""
JUEGO DE SQUASH - PROYECTO FINAL CON PATRONES DE DISEÑO
========================================================
Patrones implementados:
- Singleton: Gestor de configuración
- Factory Method: Creación de pelotas especiales
- Observer: Sistema de notificaciones de eventos
- Strategy: Diferentes estrategias de dificultad
- Decorator: Modos especiales de raqueta
- Adapter: Soporte para diferentes tipos de entrada
- State: Estados del juego (Menú, Jugando, Pausa, GameOver)
- Command: Sistema de comandos para acciones del juego

Estructura modular para Visual Studio Code
"""

import sys
import pygame
from config.configuracion import ConfiguracionJuego
from estados.gestor_estados import GestorEstados
from estados.estado_menu import EstadoMenu

def main():
    """
    Función principal del juego.
    Inicializa Pygame y el gestor de estados.
    """
    # Inicializar Pygame
    pygame.init()
    
    # Obtener configuración usando Singleton
    config = ConfiguracionJuego.obtener_instancia()
    
    # Crear pantalla
    pantalla = pygame.display.set_mode((config.ancho_pantalla, config.alto_pantalla))
    pygame.display.set_caption("🎮 Squash - Patrones de Diseño")
    
    # Crear reloj para controlar FPS
    reloj = pygame.time.Clock()
    
    # Crear gestor de estados e iniciar con el menú
    gestor_estados = GestorEstados(pantalla)
    gestor_estados.cambiar_estado(EstadoMenu(gestor_estados))
    
    # Mensaje de inicio en consola
    print("=" * 70)
    print("🎯 SQUASH - PROYECTO FINAL CON PATRONES DE DISEÑO")
    print("=" * 70)
    print("✅ Singleton: ConfiguracionJuego")
    print("✅ Factory Method: FabricaPelotas")
    print("✅ Observer: ObservadorEventos")
    print("✅ Strategy: Estrategias de dificultad")
    print("✅ Decorator: Modos especiales de raqueta")
    print("✅ Adapter: InputAdapter para múltiples controles")
    print("✅ State: Gestión de estados del juego")
    print("✅ Command: Sistema de comandos")
    print("=" * 70)
    
    # Loop principal del juego
    ejecutando = True
    while ejecutando:
        # Procesar eventos
        eventos = pygame.event.get()
        for evento in eventos:
            if evento.type == pygame.QUIT:
                ejecutando = False
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                ejecutando = False
        
        # Actualizar estado actual
        gestor_estados.actualizar(eventos)
        
        # Dibujar estado actual
        gestor_estados.dibujar()
        
        # Actualizar pantalla
        pygame.display.flip()
        
        # Controlar FPS
        reloj.tick(config.fps)
    
    # Finalizar Pygame
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()