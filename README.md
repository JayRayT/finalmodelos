Juan David Rayo Tejada - 20231020023
Jonnatan Camargo Camacho 20231020204
# 🎮 JUEGO DE SQUASH - PATRONES DE DISEÑO

Proyecto final implementando múltiples patrones de diseño en Python con Pygame.

## 📋 PATRONES IMPLEMENTADOS

### ✅ Patrones Creacionales

1. **SINGLETON** (`config/configuracion.py`)
   - Garantiza una única instancia de configuración global
   - Centraliza los parámetros del juego
   - Evita duplicación de configuraciones

2. **FACTORY METHOD** (`entidades/fabrica_pelotas.py`)
   - Crea diferentes tipos de pelotas sin especificar clases concretas
   - Pelotas: Normal, Rápida, Lenta, Multiplicadora, Vida Extra
   - Facilita la extensión con nuevos tipos

### ✅ Patrones Estructurales

3. **DECORATOR** (`entidades/raqueta.py`)
   - Agrega funcionalidades dinámicas a los modos de raqueta
   - Decorador `@modo_especial` para logging y validación
   - Modos: Normal, Rápido, Ancho, Imantación, Escudo

4. **ADAPTER** (`adaptadores/input_adapter.py`)
   - Adapta diferentes dispositivos de entrada (teclado, mouse, joystick)
   - Interfaz unificada sin modificar código base
   - Cambio dinámico de dispositivo de entrada

### ✅ Patrones de Comportamiento

5. **OBSERVER** (`observers/observador_eventos.py`)
   - Sistema de notificaciones de eventos del juego
   - Observadores: Puntaje, Sonido, Estadísticas, Logros
   - Desacopla la lógica de eventos de la respuesta

6. **STRATEGY** (`estrategias/dificultad.py`)
   - Define diferentes algoritmos de dificultad intercambiables
   - Estrategias: Fácil, Normal, Difícil, Extrema
   - Cambio dinámico de comportamiento del juego

7. **STATE** (`estados/`)
   - Gestiona diferentes estados del juego
   - Estados: Menú, Jugando, Pausa, GameOver
   - Transiciones limpias entre estados

8. **COMMAND** (`comandos/sistema_comandos.py`)
   - Encapsula acciones como objetos
   - Soporte para deshacer/rehacer
   - Historial de comandos ejecutados

## 📁 ESTRUCTURA DEL PROYECTO

```
squash_proyecto/
│
├── main.py                          # Punto de entrada principal
│
├── config/
│   └── configuracion.py             # SINGLETON - Configuración global
│
├── entidades/
│   ├── fabrica_pelotas.py          # FACTORY METHOD - Creación de pelotas
│   └── raqueta.py                  # Raqueta con DECORATOR
│
├── adaptadores/
│   └── input_adapter.py            # ADAPTER - Entrada de dispositivos
│
├── estrategias/
│   └── dificultad.py               # STRATEGY - Niveles de dificultad
│
├── estados/
│   ├── estado_base.py              # STATE - Clase base de estados
│   ├── gestor_estados.py           # Gestor de transiciones
│   ├── estado_menu.py              # Estado del menú principal
│   ├── estado_jugando.py           # Estado principal del juego
│   ├── estado_pausa.py             # Estado de pausa
│   └── estado_gameover.py          # Estado de game over
│
├── observers/
│   └── observador_eventos.py       # OBSERVER - Sistema de notificaciones
│
├── comandos/
│   └── sistema_comandos.py         # COMMAND - Sistema de comandos
│
├── requirements.txt                # Dependencias del proyecto
└── README.md                       # Esta documentación
```

## 🚀 INSTALACIÓN

### 1. Instalar Python 3.7+
Descargar desde: https://www.python.org/downloads/

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Ejecutar el juego

```bash
python main.py
```

## 🎮 CONTROLES

### Movimiento
- **← →** o **A D**: Mover raqueta izquierda/derecha
- **Mouse**: Modo alternativo de control (presiona F1 para cambiar)

### Modos de Raqueta (DECORATOR)
- **A**: Modo Rápido (+Velocidad, -Ancho)
- **S**: Modo Ancho (+Ancho, -Velocidad)
- **D**: Modo Imantación (Atrae la pelota)
- **W**: Modo Normal (Configuración base)
- **Q**: Modo Escudo (Rebote más fuerte)

### Sistema
- **P / ESC**: Pausar juego
- **F1**: Cambiar tipo de entrada (teclado ↔ mouse)

## 🎯 CARACTERÍSTICAS DEL JUEGO

### Sistema de Dificultad (STRATEGY)
Cuatro niveles con diferentes características:
- **Fácil**: 5 vidas, velocidad baja, muchos power-ups
- **Normal**: 3 vidas, velocidad media, power-ups moderados
- **Difícil**: 2 vidas, velocidad alta, pocos power-ups
- **Extrema**: 1 vida, velocidad máxima, sin power-ups

### Tipos de Pelotas (FACTORY METHOD)
- **Normal**: Pelota estándar
- **Rápida**: Más velocidad, más puntos
- **Lenta**: Menos velocidad, fácil de golpear
- **Multiplicadora**: Activa multiplicador x2 temporal
- **Vida Extra**: Otorga una vida adicional

### Sistema de Observadores (OBSERVER)
- **Puntaje**: Rastrea puntos y combos
- **Sonido**: Efectos de audio (simulados)
- **Estadísticas**: Precisión, golpes, vidas
- **Logros**: Detecta y notifica logros desbloqueados

### Sistema de Comandos (COMMAND)
- Historial de acciones
- Soporte para deshacer/rehacer
- Comandos: CambiarModo, MoverRaqueta, OtorgarVida, etc.

## 🏆 LOGROS DESBLOQUEABLES

- **Primera Sangre**: Golpear la primera pelota
- **Combo 5**: Conseguir 5 golpes consecutivos
- **Combo 10**: Conseguir 10 golpes consecutivos
- **Superviviente**: Alcanzar nivel 5
- **Maestro**: Alcanzar nivel 10

## 🧪 EJEMPLOS DE USO DE PATRONES

### SINGLETON
```python
# Obtener instancia única de configuración
config = ConfiguracionJuego.obtener_instancia()
fps = config.fps
```

### FACTORY METHOD
```python
# Crear pelota específica
pelota = FabricaPelotas.crear_pelota("rapida", x=400, y=100)

# Crear pelota aleatoria según nivel
pelota = FabricaPelotas.crear_pelota_aleatoria(nivel=3)
```

### OBSERVER
```python
# Agregar observador
observador_puntaje = ObservadorPuntaje()
juego.agregar_observador(observador_puntaje)

# Notificar evento
juego.notificar_observadores("golpe_exitoso", {"puntos": 50})
```

### STRATEGY
```python
# Cambiar estrategia de dificultad
estrategia = DificultadDificil()
gestor_dificultad.cambiar_estrategia(estrategia)
```

### DECORATOR
```python
# Activar modo especial (decorado)
raqueta.activar_modo_rapido(True)
```

### COMMAND
```python
# Crear y ejecutar comando
comando = ComandoCambiarModo(raqueta, "Rápido")
invocador.ejecutar_comando(comando)

# Deshacer comando
invocador.deshacer()
```

## 📊 ESTADÍSTICAS EN CONSOLA

El juego imprime información detallada en consola sobre:
- Activación de patrones
- Creación de objetos (Factory)
- Cambios de estado (State)
- Notificaciones de observadores
- Ejecución de comandos
- Logros desbloqueados

## 🔧 REQUISITOS DEL SISTEMA

- Python 3.7 o superior
- Pygame 2.0.0 o superior
- Sistema operativo: Windows, macOS o Linux
- RAM: 256 MB mínimo
- Espacio en disco: 50 MB

## 📝 NOTAS PARA DESARROLLO

### Agregar nuevo tipo de pelota:
1. Crear clase heredando de `Pelota` en `fabrica_pelotas.py`
2. Implementar `efecto_especial()`
3. Agregar al diccionario en `FabricaPelotas.crear_pelota()`

### Agregar nueva dificultad:
1. Crear clase heredando de `EstrategiaDificultad`
2. Implementar todos los métodos abstractos
3. Agregar al menú en `estado_menu.py`

### Agregar nuevo observador:
1. Crear clase heredando de `Observador`
2. Implementar método `actualizar(evento, datos)`
3. Registrar en `estado_jugando.py`

## 🐛 SOLUCIÓN DE PROBLEMAS

### El juego no inicia:
```bash
# Verificar instalación de Pygame
pip install pygame --upgrade
```

### Error de módulos no encontrados:
```bash
# Asegurarse de ejecutar desde el directorio raíz
cd squash_proyecto
python main.py
```

### Joystick no detectado:
- Conectar el joystick antes de iniciar el juego
- El juego cambia automáticamente a teclado si no hay joystick

## 👨‍💻 AUTOR

Proyecto Final - Patrones de Diseño
Curso de Programación Orientada a Objetos

## 📄 LICENCIA

Este proyecto es con fines educativos.

## 🎓 APRENDIZAJES

Este proyecto demuestra:
- ✅ Uso correcto de 8+ patrones de diseño
- ✅ Código modular y mantenible
- ✅ Separación de responsabilidades
- ✅ Extensibilidad y escalabilidad
- ✅ Buenas prácticas de POO
- ✅ Documentación completa

---

**¡Disfruta el juego y aprende sobre patrones de diseño! 🎮🎯**
