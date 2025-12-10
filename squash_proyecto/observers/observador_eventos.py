"""
PATRÓN OBSERVER - Sistema de Notificaciones
============================================
"""

from abc import ABC, abstractmethod

class Observador(ABC):
    """
    PATRÓN: OBSERVER - Interface
    """
    
    @abstractmethod
    def actualizar(self, evento, datos):
        pass


class ObservadorPuntaje(Observador):
    """Observa eventos relacionados con el puntaje."""
    
    def __init__(self):
        self.puntaje_total = 0
        self.combo_actual = 0
        self.mejor_combo = 0
        self.golpes_consecutivos = 0
    
    def actualizar(self, evento, datos):
        if evento == "golpe_exitoso":
            self.golpes_consecutivos += 1
            
            if datos:
                self.combo_actual = datos.get("combo", 1)
                if self.combo_actual > self.mejor_combo:
                    self.mejor_combo = self.combo_actual
                
                if self.golpes_consecutivos >= 10:
                    print("🎯 [OBSERVER] ¡Combo de 10 golpes consecutivos!")
        
        elif evento == "pelota_perdida":
            self.golpes_consecutivos = 0
            print("❌ [OBSERVER] Combo roto")


class ObservadorSonido(Observador):
    """Observa eventos para reproducir sonidos."""
    
    def actualizar(self, evento, datos):
        # En una implementación real, aquí se reproducirían sonidos
        if evento == "golpe_exitoso":
            print("🔊 [OBSERVER] Sonido: Golpe exitoso")
        elif evento == "pelota_perdida":
            print("🔊 [OBSERVER] Sonido: Pelota perdida")
        elif evento == "nivel_subido":
            print("🔊 [OBSERVER] Sonido: ¡Nivel subido!")
        elif evento == "game_over":
            print("🔊 [OBSERVER] Sonido: Game Over")


class ObservadorEstadisticas(Observador):
    """Recopila estadísticas del juego."""
    
    def __init__(self):
        self.golpes_totales = 0
        self.golpes_acertados = 0
        self.golpes_fallados = 0
    
    def actualizar(self, evento, datos):
        if evento == "golpe_exitoso":
            self.golpes_totales += 1
            self.golpes_acertados += 1
        elif evento == "pelota_perdida":
            self.golpes_totales += 1
            self.golpes_fallados += 1
        elif evento == "game_over":
            print(f"📊 [OBSERVER] Estadísticas finales:")
            print(f"   Golpes totales: {self.golpes_totales}")
            print(f"   Golpes acertados: {self.golpes_acertados}")
            print(f"   Golpes fallados: {self.golpes_fallados}")
            print(f"   Precisión: {self.calcular_precision():.1f}%")
    
    def calcular_precision(self):
        if self.golpes_totales == 0:
            return 0
        return (self.golpes_acertados / self.golpes_totales) * 100


class ObservadorLogros(Observador):
    """Maneja el sistema de logros."""
    
    def __init__(self):
        self.logros_desbloqueados = []
    
    def actualizar(self, evento, datos):
        if evento == "golpe_exitoso" and datos:
            combo = datos.get("combo", 0)
            
            if combo >= 5 and "combo_5" not in self.logros_desbloqueados:
                self.logros_desbloqueados.append("combo_5")
                print("🏆 [OBSERVER] Logro desbloqueado: Combo x5")
            
            if combo >= 10 and "combo_10" not in self.logros_desbloqueados:
                self.logros_desbloqueados.append("combo_10")
                print("🏆 [OBSERVER] Logro desbloqueado: Combo x10")
        
        elif evento == "nivel_subido" and datos:
            nivel = datos.get("nivel", 0)
            
            if nivel >= 3 and "nivel_3" not in self.logros_desbloqueados:
                self.logros_desbloqueados.append("nivel_3")
                print("🏆 [OBSERVER] Logro desbloqueado: Nivel 3 alcanzado")
            
            if nivel >= 5 and "nivel_5" not in self.logros_desbloqueados:
                self.logros_desbloqueados.append("nivel_5")
                print("🏆 [OBSERVER] Logro desbloqueado: Nivel 5 alcanzado")