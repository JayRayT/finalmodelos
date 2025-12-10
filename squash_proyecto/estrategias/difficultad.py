# pylint: disable=all
"""
PATRÓN STRATEGY - Estrategias de Dificultad
============================================
Define diferentes algoritmos de dificultad intercambiables.
"""

from abc import ABC, abstractmethod

# =============================================================================
# PATRÓN STRATEGY - INTERFACE
# =============================================================================

class EstrategiaDificultad(ABC):
    """
    PATRÓN: STRATEGY
    ----------------
    Interface para diferentes estrategias de dificultad.
    Permite cambiar el comportamiento del juego dinámicamente.
    """
    
    @abstractmethod
    def obtener_nombre(self):
        """Retorna el nombre de la dificultad."""
        pass
    
    @abstractmethod
    def calcular_velocidad_pelota(self, nivel):
        """Calcula la velocidad de la pelota según el nivel."""
        pass
    
    @abstractmethod
    def calcular_vidas_iniciales(self):
        """Calcula las vidas iniciales."""
        pass
    
    @abstractmethod
    def calcular_puntos_por_golpe(self, nivel):
        """Calcula los puntos otorgados por golpe."""
        pass
    
    @abstractmethod
    def obtener_probabilidad_pelota_especial(self, nivel):
        """Calcula la probabilidad de pelotas especiales."""
        pass
    
    @abstractmethod
    def obtener_descripcion(self):
        """Retorna una descripción de la dificultad."""
        pass


# =============================================================================
# ESTRATEGIAS CONCRETAS
# =============================================================================

class DificultadFacil(EstrategiaDificultad):
    """
    Estrategia de dificultad FÁCIL.
    - Velocidad baja
    - Más vidas
    - Más puntos
    - Más power-ups
    """
    
    def obtener_nombre(self):
        return "Fácil"
    
    def calcular_velocidad_pelota(self, nivel):
        """Velocidad moderada que crece lentamente."""
        velocidad_base = 4
        incremento = 0.3 * nivel
        return velocidad_base + incremento
    
    def calcular_vidas_iniciales(self):
        """Más vidas para principiantes."""
        return 5
    
    def calcular_puntos_por_golpe(self, nivel):
        """Más puntos para recompensar al jugador."""
        return 15 * nivel
    
    def obtener_probabilidad_pelota_especial(self, nivel):
        """Alta probabilidad de power-ups."""
        return min(50 + (nivel * 5), 80)
    
    def obtener_descripcion(self):
        return "Perfecto para aprender | +Vidas +PowerUps"


class DificultadNormal(EstrategiaDificultad):
    """
    Estrategia de dificultad NORMAL.
    - Velocidad equilibrada
    - Vidas estándar
    - Puntos balanceados
    """
    
    def obtener_nombre(self):
        return "Normal"
    
    def calcular_velocidad_pelota(self, nivel):
        """Velocidad balanceada."""
        velocidad_base = 5
        incremento = 0.5 * nivel
        return velocidad_base + incremento
    
    def calcular_vidas_iniciales(self):
        """Vidas estándar."""
        return 3
    
    def calcular_puntos_por_golpe(self, nivel):
        """Puntos balanceados."""
        return 10 * nivel
    
    def obtener_probabilidad_pelota_especial(self, nivel):
        """Probabilidad moderada de power-ups."""
        return min(30 + (nivel * 5), 60)
    
    def obtener_descripcion(self):
        return "Experiencia equilibrada | Dificultad estándar"


class DificultadDificil(EstrategiaDificultad):
    """
    Estrategia de dificultad DIFÍCIL.
    - Alta velocidad
    - Pocas vidas
    - Pocos power-ups
    - Más puntos por el desafío
    """
    
    def obtener_nombre(self):
        return "Difícil"
    
    def calcular_velocidad_pelota(self, nivel):
        """Alta velocidad desde el inicio."""
        velocidad_base = 6.5
        incremento = 0.7 * nivel
        return velocidad_base + incremento
    
    def calcular_vidas_iniciales(self):
        """Pocas vidas para aumentar el desafío."""
        return 2
    
    def calcular_puntos_por_golpe(self, nivel):
        """Más puntos por el reto."""
        return 20 * nivel
    
    def obtener_probabilidad_pelota_especial(self, nivel):
        """Baja probabilidad de power-ups."""
        return min(15 + (nivel * 3), 40)
    
    def obtener_descripcion(self):
        return "Para expertos | -Vidas +Velocidad +Puntos"


class DificultadExtrema(EstrategiaDificultad):
    """
    Estrategia de dificultad EXTREMA.
    - Velocidad muy alta
    - Una sola vida
    - Sin power-ups
    - Muchos puntos
    """
    
    def obtener_nombre(self):
        return "Extrema"
    
    def calcular_velocidad_pelota(self, nivel):
        """Velocidad extrema."""
        velocidad_base = 8
        incremento = 1.0 * nivel
        return velocidad_base + incremento
    
    def calcular_vidas_iniciales(self):
        """Una sola vida."""
        return 1
    
    def calcular_puntos_por_golpe(self, nivel):
        """Muchos puntos por el riesgo."""
        return 50 * nivel
    
    def obtener_probabilidad_pelota_especial(self, nivel):
        """Sin power-ups."""
        return 0
    
    def obtener_descripcion(self):
        return "¡1 VIDA! | Velocidad máxima | Sin power-ups"


# =============================================================================
# CONTEXTO QUE USA LA ESTRATEGIA
# =============================================================================

class GestorDificultad:
    """
    Contexto que utiliza una estrategia de dificultad.
    Permite cambiar la estrategia en tiempo de ejecución.
    """
    
    def __init__(self, estrategia=None):
        """
        Inicializa con una estrategia.
        Por defecto usa dificultad Normal.
        """
        if estrategia is None:
            estrategia = DificultadNormal()
        
        self._estrategia = estrategia
        print(f"⚙️ [STRATEGY] Dificultad: {self._estrategia.obtener_nombre()}")
    
    def cambiar_estrategia(self, nueva_estrategia):
        """Cambia la estrategia de dificultad."""
        self._estrategia = nueva_estrategia
        print(f"⚙️ [STRATEGY] Dificultad cambiada a: {self._estrategia.obtener_nombre()}")
    
    def obtener_estrategia(self):
        """Retorna la estrategia actual."""
        return self._estrategia
    
    def aplicar_configuracion(self, juego, nivel):
        """
        Aplica la configuración de dificultad al juego.
        """
        # Configurar vidas si es inicio del juego
        if nivel == 1:
            juego.vidas = self._estrategia.calcular_vidas_iniciales()
        
        # Configurar velocidad de pelota
        if hasattr(juego, 'pelota') and juego.pelota:
            velocidad = self._estrategia.calcular_velocidad_pelota(nivel)
            factor = velocidad / 5  # 5 es la velocidad base
            juego.pelota.velocidad_x = juego.pelota.velocidad_x / abs(juego.pelota.velocidad_x) * velocidad
            juego.pelota.velocidad_y = abs(juego.pelota.velocidad_y) * factor
        
        print(f"⚙️ [STRATEGY] Configuración aplicada - Nivel {nivel}")
    
    @staticmethod
    def obtener_estrategias_disponibles():
        """Retorna un diccionario con todas las estrategias disponibles."""
        return {
            "facil": DificultadFacil(),
            "normal": DificultadNormal(),
            "dificil": DificultadDificil(),
            "extrema": DificultadExtrema()
        }