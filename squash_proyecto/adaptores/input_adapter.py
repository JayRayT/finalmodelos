# pylint: disable=all
"""
PATRÓN ADAPTER - Adaptador de Entradas
=======================================
Permite usar diferentes dispositivos de entrada sin cambiar el código base.
"""

import pygame

# =============================================================================
# PATRÓN ADAPTER
# =============================================================================

class InputAdapter:
    """
    PATRÓN: ADAPTER
    ---------------
    Adapta diferentes tipos de entrada (teclado, mouse, joystick)
    a una interfaz común de teclas presionadas.
    
    Propósito: Permitir que el juego funcione con diferentes
    dispositivos sin modificar la lógica principal.
    """
    
    def __init__(self, tipo_entrada="teclado"):
        """
        Inicializa el adaptador con el tipo de entrada deseado.
        
        Args:
            tipo_entrada: 'teclado', 'mouse' o 'joystick'
        """
        self.tipo_entrada = tipo_entrada
        self.joystick = None
        
        # Intentar inicializar joystick si se solicita
        if tipo_entrada == "joystick":
            self._inicializar_joystick()
        
        print(f"🎮 [ADAPTER] Tipo de entrada: {self.tipo_entrada}")
    
    def _inicializar_joystick(self):
        """Inicializa el joystick si está disponible."""
        pygame.joystick.init()
        
        if pygame.joystick.get_count() > 0:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()
            print(f"🎮 [ADAPTER] Joystick detectado: {self.joystick.get_name()}")
        else:
            print("⚠️ [ADAPTER] No se detectó joystick. Usando teclado.")
            self.tipo_entrada = "teclado"
    
    def obtener_entrada(self):
        """
        Obtiene la entrada del dispositivo actual y la adapta
        al formato de teclas presionadas de Pygame.
        
        Returns:
            Lista simulando pygame.key.get_pressed()
        """
        if self.tipo_entrada == "teclado":
            return self._obtener_entrada_teclado()
        
        elif self.tipo_entrada == "mouse":
            return self._obtener_entrada_mouse()
        
        elif self.tipo_entrada == "joystick":
            return self._obtener_entrada_joystick()
        
        # Por defecto, usar teclado
        return self._obtener_entrada_teclado()
    
    def _obtener_entrada_teclado(self):
        """Obtiene entrada del teclado (sin adaptación)."""
        return pygame.key.get_pressed()
    
    def _obtener_entrada_mouse(self):
        """
        Adapta la posición del mouse a teclas de movimiento.
        Mouse a la izquierda = tecla LEFT
        Mouse a la derecha = tecla RIGHT
        """
        x_mouse, _ = pygame.mouse.get_pos()
        centro_pantalla = 1000 // 2
        
        # Crear lista simulando teclas presionadas
        teclas_simuladas = [False] * 512
        
        # Zona muerta en el centro para evitar movimientos erráticos
        zona_muerta = 100
        
        if x_mouse < centro_pantalla - zona_muerta:
            teclas_simuladas[pygame.K_LEFT] = True
        elif x_mouse > centro_pantalla + zona_muerta:
            teclas_simuladas[pygame.K_RIGHT] = True
        
        # Copiar teclas reales para los modos
        teclas_reales = pygame.key.get_pressed()
        teclas_simuladas[pygame.K_a] = teclas_reales[pygame.K_a]
        teclas_simuladas[pygame.K_s] = teclas_reales[pygame.K_s]
        teclas_simuladas[pygame.K_d] = teclas_reales[pygame.K_d]
        teclas_simuladas[pygame.K_w] = teclas_reales[pygame.K_w]
        teclas_simuladas[pygame.K_q] = teclas_reales[pygame.K_q]
        
        return teclas_simuladas
    
    def _obtener_entrada_joystick(self):
        """
        Adapta los ejes del joystick a teclas de movimiento.
        Eje X negativo = tecla LEFT
        Eje X positivo = tecla RIGHT
        """
        if not self.joystick:
            return self._obtener_entrada_teclado()
        
        # Obtener valor del eje X (horizontal)
        try:
            eje_x = self.joystick.get_axis(0)
        except:
            return self._obtener_entrada_teclado()
        
        # Crear lista simulando teclas presionadas
        teclas_simuladas = [False] * 512
        
        # Zona muerta para evitar drift del joystick
        zona_muerta = 0.2
        
        if eje_x < -zona_muerta:
            teclas_simuladas[pygame.K_LEFT] = True
        elif eje_x > zona_muerta:
            teclas_simuladas[pygame.K_RIGHT] = True
        
        # Mapear botones del joystick a modos
        try:
            # Botón 0 (A/X) = Modo Rápido
            if self.joystick.get_button(0):
                teclas_simuladas[pygame.K_a] = True
            
            # Botón 1 (B/Circle) = Modo Ancho
            if self.joystick.get_button(1):
                teclas_simuladas[pygame.K_s] = True
            
            # Botón 2 (X/Square) = Modo Imantación
            if self.joystick.get_button(2):
                teclas_simuladas[pygame.K_d] = True
            
            # Botón 3 (Y/Triangle) = Modo Normal
            if self.joystick.get_button(3):
                teclas_simuladas[pygame.K_w] = True
        except:
            pass
        
        return teclas_simuladas
    
    def cambiar_tipo_entrada(self, nuevo_tipo):
        """
        Cambia el tipo de entrada dinámicamente.
        
        Args:
            nuevo_tipo: 'teclado', 'mouse' o 'joystick'
        """
        tipo_anterior = self.tipo_entrada
        self.tipo_entrada = nuevo_tipo
        
        if nuevo_tipo == "joystick" and not self.joystick:
            self._inicializar_joystick()
        
        print(f"🎮 [ADAPTER] Entrada cambiada: {tipo_anterior} → {nuevo_tipo}")
    
    def obtener_tipo_actual(self):
        """Retorna el tipo de entrada actual."""
        return self.tipo_entrada