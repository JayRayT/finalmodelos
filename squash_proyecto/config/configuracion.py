"""
PATRÓN SINGLETON - Configuración del Juego
===========================================
"""

class ConfiguracionJuego:
    """
    PATRÓN: SINGLETON
    -----------------
    Gestiona la configuración global del juego.
    Asegura una única instancia en todo el programa.
    """
    
    _instancia = None
    
    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            cls._instancia._inicializar()
        return cls._instancia
    
    @classmethod
    def obtener_instancia(cls):
        """Método estático para obtener la instancia Singleton."""
        if cls._instancia is None:
            cls()
        return cls._instancia
    
    def _inicializar(self):
        """Inicializa la configuración por defecto."""
        self.ancho_pantalla = 1000
        self.alto_pantalla = 700
        self.fps = 60
        self.color_fondo = (0, 0, 30)
        
        # Colores de la interfaz
        self.color_texto = (255, 255, 255)
        self.color_secundario = (100, 200, 255)
        self.color_exito = (0, 255, 0)
        self.color_error = (255, 0, 0)
        
        # Configuración de audio
        self.volumen_musica = 0.5
        self.volumen_efectos = 0.7
        
        # Configuración de juego
        self.max_nivel = 10
        self.max_pelotas_especiales = 3
        
        print("⚙️ [SINGLETON] Configuración inicializada")
    
    def guardar_configuracion(self):
        """Guarda la configuración en un archivo (para futuras implementaciones)."""
        print("💾 [SINGLETON] Configuración guardada")
    
    def cargar_configuracion(self):
        """Carga la configuración desde un archivo (para futuras implementaciones)."""
        print("📂 [SINGLETON] Configuración cargada")