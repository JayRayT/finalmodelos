# pylint: disable=all
"""
PATRÓN COMMAND - Sistema de Comandos
=====================================
Encapsula acciones como objetos, permitiendo deshacer/rehacer.
"""

from abc import ABC, abstractmethod

# =============================================================================
# PATRÓN COMMAND - INTERFACE
# =============================================================================

class Comando(ABC):
    """
    PATRÓN: COMMAND
    ---------------
    Interface para todos los comandos del juego.
    Encapsula una acción y su lógica de ejecución/deshecho.
    """
    
    @abstractmethod
    def ejecutar(self):
        """Ejecuta el comando."""
        pass
    
    @abstractmethod
    def deshacer(self):
        """Deshace el comando."""
        pass
    
    def obtener_descripcion(self):
        """Retorna una descripción del comando."""
        return self.__class__.__name__


# =============================================================================
# COMANDOS CONCRETOS
# =============================================================================

class ComandoCambiarModo(Comando):
    """Comando para cambiar el modo de la raqueta."""
    
    def __init__(self, raqueta, nuevo_modo):
        self.raqueta = raqueta
        self.nuevo_modo = nuevo_modo
        self.modo_anterior = None
    
    def ejecutar(self):
        """Cambia al nuevo modo."""
        self.modo_anterior = self.raqueta.modo_actual
        self.raqueta.cambiar_modo(self.nuevo_modo)
        print(f"⚡ [COMMAND] Modo cambiado a: {self.nuevo_modo}")
    
    def deshacer(self):
        """Vuelve al modo anterior."""
        if self.modo_anterior:
            self.raqueta.cambiar_modo(self.modo_anterior)
            print(f"↩️ [COMMAND] Modo revertido a: {self.modo_anterior}")
    
    def obtener_descripcion(self):
        return f"CambiarModo({self.nuevo_modo})"


class ComandoMoverRaqueta(Comando):
    """Comando para mover la raqueta."""
    
    def __init__(self, raqueta, direccion, distancia):
        self.raqueta = raqueta
        self.direccion = direccion  # 'izquierda' o 'derecha'
        self.distancia = distancia
        self.posicion_anterior = None
    
    def ejecutar(self):
        """Mueve la raqueta."""
        self.posicion_anterior = self.raqueta.x
        
        if self.direccion == 'izquierda':
            self.raqueta.x = max(0, self.raqueta.x - self.distancia)
        elif self.direccion == 'derecha':
            limite = 1000 - self.raqueta.ancho
            self.raqueta.x = min(limite, self.raqueta.x + self.distancia)
    
    def deshacer(self):
        """Restaura la posición anterior."""
        if self.posicion_anterior is not None:
            self.raqueta.x = self.posicion_anterior


class ComandoOtorgarVida(Comando):
    """Comando para otorgar una vida al jugador."""
    
    def __init__(self, juego):
        self.juego = juego
        self.vida_otorgada = False
    
    def ejecutar(self):
        """Otorga una vida."""
        self.juego.vidas += 1
        self.vida_otorgada = True
        print(f"❤️ [COMMAND] Vida otorgada. Total: {self.juego.vidas}")
    
    def deshacer(self):
        """Quita la vida otorgada."""
        if self.vida_otorgada and self.juego.vidas > 0:
            self.juego.vidas -= 1
            self.vida_otorgada = False
            print(f"↩️ [COMMAND] Vida revertida. Total: {self.juego.vidas}")


class ComandoAgregarPuntos(Comando):
    """Comando para agregar puntos."""
    
    def __init__(self, juego, puntos):
        self.juego = juego
        self.puntos = puntos
        self.puntos_agregados = False
    
    def ejecutar(self):
        """Agrega puntos al puntaje."""
        self.juego.puntaje += self.puntos
        self.puntos_agregados = True
    
    def deshacer(self):
        """Quita los puntos agregados."""
        if self.puntos_agregados:
            self.juego.puntaje -= self.puntos
            self.puntos_agregados = False


class ComandoCambiarDificultad(Comando):
    """Comando para cambiar la dificultad del juego."""
    
    def __init__(self, gestor_dificultad, nueva_estrategia):
        self.gestor_dificultad = gestor_dificultad
        self.nueva_estrategia = nueva_estrategia
        self.estrategia_anterior = None
    
    def ejecutar(self):
        """Cambia la estrategia de dificultad."""
        self.estrategia_anterior = self.gestor_dificultad.obtener_estrategia()
        self.gestor_dificultad.cambiar_estrategia(self.nueva_estrategia)
        print(f"⚙️ [COMMAND] Dificultad cambiada a: {self.nueva_estrategia.obtener_nombre()}")
    
    def deshacer(self):
        """Vuelve a la estrategia anterior."""
        if self.estrategia_anterior:
            self.gestor_dificultad.cambiar_estrategia(self.estrategia_anterior)
            print(f"↩️ [COMMAND] Dificultad revertida a: {self.estrategia_anterior.obtener_nombre()}")


# =============================================================================
# INVOCADOR DE COMANDOS
# =============================================================================

class InvocadorComandos:
    """
    Invocador que ejecuta comandos y mantiene historial
    para deshacer/rehacer.
    """
    
    def __init__(self):
        self.historial = []
        self.indice_actual = -1
        self.limite_historial = 50
    
    def ejecutar_comando(self, comando):
        """
        Ejecuta un comando y lo agrega al historial.
        """
        comando.ejecutar()
        
        # Eliminar comandos posteriores si estamos en medio del historial
        self.historial = self.historial[:self.indice_actual + 1]
        
        # Agregar nuevo comando
        self.historial.append(comando)
        self.indice_actual += 1
        
        # Limitar tamaño del historial
        if len(self.historial) > self.limite_historial:
            self.historial.pop(0)
            self.indice_actual -= 1
    
    def deshacer(self):
        """Deshace el último comando."""
        if self.puede_deshacer():
            comando = self.historial[self.indice_actual]
            comando.deshacer()
            self.indice_actual -= 1
            print(f"↩️ [COMMAND] Deshecho: {comando.obtener_descripcion()}")
            return True
        
        print("⚠️ [COMMAND] No hay comandos para deshacer")
        return False
    
    def rehacer(self):
        """Rehace el siguiente comando."""
        if self.puede_rehacer():
            self.indice_actual += 1
            comando = self.historial[self.indice_actual]
            comando.ejecutar()
            print(f"↪️ [COMMAND] Rehecho: {comando.obtener_descripcion()}")
            return True
        
        print("⚠️ [COMMAND] No hay comandos para rehacer")
        return False
    
    def puede_deshacer(self):
        """Verifica si se puede deshacer."""
        return self.indice_actual >= 0
    
    def puede_rehacer(self):
        """Verifica si se puede rehacer."""
        return self.indice_actual < len(self.historial) - 1
    
    def limpiar_historial(self):
        """Limpia el historial de comandos."""
        self.historial.clear()
        self.indice_actual = -1
        print("🧹 [COMMAND] Historial limpiado")
    
    def mostrar_historial(self):
        """Muestra el historial de comandos."""
        print("\n📜 [COMMAND] HISTORIAL DE COMANDOS")
        print("=" * 50)
        for i, comando in enumerate(self.historial):
            marcador = "→" if i == self.indice_actual else " "
            print(f"{marcador} {i+1}. {comando.obtener_descripcion()}")
        print("=" * 50 + "\n")