# pylint: disable=all
"""
Estado Principal del Juego
===========================
Integra todos los patrones de diseño.
"""

import pygame
import random
from estados.estado_base import Estado
from estados.estado_pausa import EstadoPausa
from estados.estado_gameover import EstadoGameOver
from entidades.raqueta import Raqueta
from entidades.fabrica_pelotas import FabricaPelotas
from adaptores.input_adapter import InputAdapter
from estrategias.difficultad import GestorDificultad
from observers.observador_eventos import *
from comandos.sistema_comandos import *
from config.configuracion import ConfiguracionJuego

class EstadoJugando(Estado):
    """
    Estado principal del juego.
    Integra todos los patrones de diseño implementados.
    """
    
    def __init__(self, gestor_estados, estrategia_dificultad=None):
        super().__init__(gestor_estados)
        
        # Obtener configuración Singleton
        self.config = ConfiguracionJuego.obtener_instancia()
        
        # Inicializar estrategia de dificultad (STRATEGY)
        self.gestor_dificultad = GestorDificultad(estrategia_dificultad)
        
        # Inicializar variables del juego
        self.puntaje = 0
        self.nivel = 1
        self.vidas = self.gestor_dificultad.obtener_estrategia().calcular_vidas_iniciales()
        self.multiplicador_activo = False
        self.tiempo_multiplicador = 0
        
        # Crear raqueta con DECORATOR
        self.raqueta = Raqueta(450, 650)
        
        # Crear pelota inicial con FACTORY METHOD
        self.pelota = FabricaPelotas.crear_pelota_aleatoria(self.nivel)
        
        # Configurar ADAPTER para entrada
        self.input_adapter = InputAdapter(tipo_entrada="teclado")
        
        # Sistema de OBSERVER
        self.observador_puntaje = ObservadorPuntaje()
        self.observador_sonido = ObservadorSonido()
        self.observador_estadisticas = ObservadorEstadisticas()
        self.observador_logros = ObservadorLogros()
        
        # Invoker de COMMAND
        self.invocador = InvocadorComandos()
        
        # Fuentes
        self.fuente = pygame.font.Font(None, 36)
        self.fuente_pequena = pygame.font.Font(None, 24)
        
        # Control de teclas para modos
        self.teclas_activadas = {
            pygame.K_a: False,
            pygame.K_s: False,
            pygame.K_d: False,
            pygame.K_w: False,
            pygame.K_q: False
        }
        
        # Aplicar configuración de dificultad
        self.gestor_dificultad.aplicar_configuracion(self, self.nivel)
        
        print("🎮 [JUGANDO] Estado de juego inicializado")
    
    def manejar_eventos(self, eventos):
        """Maneja eventos durante el juego."""
        for evento in eventos:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_p or evento.key == pygame.K_ESCAPE:
                    # Pausar el juego
                    self.gestor_estados.apilar_estado(EstadoPausa(self.gestor_estados))
                
                elif evento.key == pygame.K_F1:
                    # Cambiar tipo de entrada (demo)
                    tipos = ["teclado", "mouse"]
                    tipo_actual = self.input_adapter.obtener_tipo_actual()
                    indice = tipos.index(tipo_actual)
                    nuevo_tipo = tipos[(indice + 1) % len(tipos)]
                    self.input_adapter.cambiar_tipo_entrada(nuevo_tipo)
    
    def actualizar(self):
        """Actualiza la lógica del juego."""
        # Obtener entrada adaptada (ADAPTER)
        teclas = self.input_adapter.obtener_entrada()
        
        # Manejar cambios de modo de la raqueta (DECORATOR)
        self.manejar_modos(teclas)
        
        # Mover raqueta
        self.raqueta.mover(teclas)
        
        # Aplicar efecto de imantación si está activo
        if self.raqueta.modo_actual == "Imantación":
            self.raqueta.aplicar_imantacion(self.pelota)
        
        # Mover pelota
        self.pelota.mover()
        
        # Verificar colisión con raqueta
        if self.pelota.verificar_colision(self.raqueta):
            # Ejecutar comando de agregar puntos (COMMAND)
            estrategia = self.gestor_dificultad.obtener_estrategia()
            puntos_base = estrategia.calcular_puntos_por_golpe(self.nivel)
            puntos_bonus = self.pelota.puntos_bonus
            
            if self.multiplicador_activo:
                puntos_totales = (puntos_base + puntos_bonus) * 2
            else:
                puntos_totales = puntos_base + puntos_bonus
            
            comando_puntos = ComandoAgregarPuntos(self, puntos_totales)
            self.invocador.ejecutar_comando(comando_puntos)
            
            # Notificar observadores (OBSERVER)
            self.observador_puntaje.actualizar("golpe_exitoso", {
                "puntos": puntos_totales,
                "combo": self.observador_puntaje.combo_actual + 1
            })
            self.observador_sonido.actualizar("golpe_exitoso", None)
            self.observador_estadisticas.actualizar("golpe_exitoso", None)
            self.observador_logros.actualizar("golpe_exitoso", {
                "combo": self.observador_puntaje.combo_actual
            })
            
            # Aplicar efecto especial de la pelota
            self.pelota.efecto_especial(self)
            
            # Modo escudo: rebote más fuerte
            if self.raqueta.modo_actual == "Escudo":
                self.pelota.velocidad_y *= 1.2
        
        # Verificar si la pelota se perdió
        if not self.pelota.activa:
            self.vidas -= 1
            
            # Notificar observadores
            self.observador_puntaje.actualizar("pelota_perdida", None)
            self.observador_sonido.actualizar("pelota_perdida", None)
            self.observador_estadisticas.actualizar("pelota_perdida", None)
            
            if self.vidas > 0:
                # Crear nueva pelota (FACTORY METHOD)
                self.pelota = FabricaPelotas.crear_pelota_aleatoria(self.nivel)
                self.gestor_dificultad.aplicar_configuracion(self, self.nivel)
                
                # Volver a modo normal
                self.raqueta.activar_modo_normal(True)
            else:
                # Game Over
                self.observador_sonido.actualizar("game_over", None)
                self.observador_estadisticas.actualizar("game_over", None)
                self.gestor_estados.cambiar_estado(EstadoGameOver(self.gestor_estados, self))
        
        # Verificar subida de nivel
        estrategia = self.gestor_dificultad.obtener_estrategia()
        puntos_necesarios = self.nivel * 100
        
        if self.puntaje >= puntos_necesarios:
            self.nivel += 1
            
            # Notificar observadores
            self.observador_sonido.actualizar("nivel_subido", None)
            self.observador_logros.actualizar("nivel_subido", {"nivel": self.nivel})
            
            # Aplicar nueva configuración de dificultad
            self.gestor_dificultad.aplicar_configuracion(self, self.nivel)
            
            print(f"🎊 ¡NIVEL {self.nivel}!")
        
        # Actualizar multiplicador
        if self.multiplicador_activo:
            self.tiempo_multiplicador -= 1
            if self.tiempo_multiplicador <= 0:
                self.multiplicador_activo = False
                print("⏰ Multiplicador desactivado")
    
    def manejar_modos(self, teclas):
        """Maneja el cambio de modos de la raqueta."""
        teclas_actuales = {
            pygame.K_a: teclas[pygame.K_a],
            pygame.K_s: teclas[pygame.K_s],
            pygame.K_d: teclas[pygame.K_d],
            pygame.K_w: teclas[pygame.K_w],
            pygame.K_q: teclas[pygame.K_q]
        }
        
        for tecla, presionada in teclas_actuales.items():
            if presionada and not self.teclas_activadas[tecla]:
                # Crear y ejecutar comando de cambio de modo (COMMAND)
                if tecla == pygame.K_a:
                    comando = ComandoCambiarModo(self.raqueta, "Rápido")
                    self.invocador.ejecutar_comando(comando)
                elif tecla == pygame.K_s:
                    comando = ComandoCambiarModo(self.raqueta, "Ancho")
                    self.invocador.ejecutar_comando(comando)
                elif tecla == pygame.K_d:
                    comando = ComandoCambiarModo(self.raqueta, "Imantación")
                    self.invocador.ejecutar_comando(comando)
                elif tecla == pygame.K_w:
                    comando = ComandoCambiarModo(self.raqueta, "Normal")
                    self.invocador.ejecutar_comando(comando)
                elif tecla == pygame.K_q:
                    comando = ComandoCambiarModo(self.raqueta, "Escudo")
                    self.invocador.ejecutar_comando(comando)
            
            self.teclas_activadas[tecla] = presionada
    
    def activar_multiplicador(self, duracion=5):
        """Activa el multiplicador de puntos temporalmente."""
        self.multiplicador_activo = True
        self.tiempo_multiplicador = duracion * 60  # Convertir a frames
    
    def dibujar(self):
        """Dibuja el estado del juego."""
        self.pantalla.fill(self.config.color_fondo)
        
        # Dibujar entidades
        self.pelota.dibujar(self.pantalla)
        self.raqueta.dibujar(self.pantalla)
        
        # HUD - Información del juego
        self.dibujar_hud()
        
        # Instrucciones
        self.dibujar_instrucciones()
    
    def dibujar_hud(self):
        """Dibuja el HUD con información del juego."""
        # Puntaje
        texto_puntaje = self.fuente.render(f"Puntos: {self.puntaje}", True, (255, 255, 255))
        self.pantalla.blit(texto_puntaje, (10, 10))
        
        # Vidas
        color_vidas = (255, 50, 50) if self.vidas <= 1 else (255, 255, 255)
        texto_vidas = self.fuente.render(f"❤️ {self.vidas}", True, color_vidas)
        self.pantalla.blit(texto_vidas, (10, 50))
        
        # Nivel
        texto_nivel = self.fuente.render(f"Nivel: {self.nivel}", True, (255, 255, 255))
        self.pantalla.blit(texto_nivel, (10, 90))
        
        # Modo actual
        texto_modo = self.fuente.render(f"Modo: {self.raqueta.modo_actual}", True, self.raqueta.color)
        self.pantalla.blit(texto_modo, (10, 130))
        
        # Combo
        if self.observador_puntaje.combo_actual > 0:
            texto_combo = self.fuente.render(f"COMBO x{self.observador_puntaje.combo_actual}!", True, (255, 255, 0))
            self.pantalla.blit(texto_combo, (10, 170))
        
        # Multiplicador
        if self.multiplicador_activo:
            segundos = self.tiempo_multiplicador // 60
            texto_multi = self.fuente.render(f"🔥 x2 PUNTOS ({segundos}s)", True, (255, 100, 0))
            self.pantalla.blit(texto_multi, (10, 210))
        
        # Tipo de pelota
        texto_pelota = self.fuente_pequena.render(f"Pelota: {self.pelota.tipo}", True, self.pelota.color)
        self.pantalla.blit(texto_pelota, (10, 250))
        
        # Dificultad
        estrategia = self.gestor_dificultad.obtener_estrategia()
        texto_dif = self.fuente_pequena.render(f"Dificultad: {estrategia.obtener_nombre()}", True, (150, 150, 255))
        self.pantalla.blit(texto_dif, (10, 275))
    
    def dibujar_instrucciones(self):
        """Dibuja las instrucciones en pantalla."""
        instrucciones = [
            "🎮 CONTROLES:",
            "← → : Movimiento",
            "A : Modo Rápido",
            "S : Modo Ancho",
            "D : Imantación",
            "W : Normal",
            "Q : Escudo",
            "P/ESC : Pausa",
            "F1 : Cambiar entrada"
        ]
        
        y_inicio = 10
        for i, inst in enumerate(instrucciones):
            color = (255, 255, 0) if i == 0 else (200, 200, 200)
            texto = self.fuente_pequena.render(inst, True, color)
            self.pantalla.blit(texto, (750, y_inicio + i * 25))