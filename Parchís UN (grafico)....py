import pygame
import sys
import random

# ---------------------------
# AJUSTES BÁSICOS DEL TABLERO
# ---------------------------
NUM_CASILLAS = 17
TAM_CASILLA = 40
ANCHO = ALTO = NUM_CASILLAS * TAM_CASILLA  # 680×680
OFFSET = TAM_CASILLA // 2

pygame.init()
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Parchís 17×17 - Sin texto en casillas, fichas numeradas")

clock = pygame.time.Clock()

# ---------------------------
# COLORES
# ---------------------------
COLORES_RGB = {
    "rojo": (255, 0, 0),
    "verde": (0, 255, 0),
    "azul": (0, 0, 255),
    "amarillo": (255, 255, 0),
}

BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
MAGENTA = (255, 0, 255)  # Para salidas

# Para la cruz en el centro
CRUZ_COLOR = (120, 120, 120)       # Gris medio
CRUZ_COLOR_FUERTE = (80, 80, 80)   # Gris más fuerte

# ---------------------------
# CASAS DE 7×7 (omitiendo la casilla interna)
# ---------------------------
POSICIONES_INICIALES = {
    "rojo": [(0, 0), (0, 1), (1, 0), (1, 1)],
    "verde": [(0, 15), (0, 16), (1, 15), (1, 16)],
    "azul": [(15, 15), (15, 16), (16, 15), (16, 16)],
    "amarillo": [(15, 0), (15, 1), (16, 0), (16, 1)],
}

# ---------------------------
# CASILLAS DE SALIDA
# ---------------------------
CASILLA_SALIDA = {
    "amarillo": (9, 4),
    "rojo": (4, 7),
    "azul": (12, 9),
    "verde": (7, 12),
}

# ---------------------------
# RUTAS PERSONALIZADAS (Saltos exactos)
# ---------------------------
RUTA_AMARILLO = [
    (9,4), (9,6), (10,6), (10,7), (16,7), (16,9), (10,9),
    (10,10), (9,10), (9,16), (7,16), (7,10), (6,10), (6,9),
    (0,9), (0,7), (6,7), (6,6), (7,6), (7,0), (8,0), (8,8)
]
RUTA_AZUL = [
    (12,9), (10,9), (10,10), (9,10), (9,16), (7,16), (7,10),
    (6,10), (6,9), (0,9), (0,7), (6,7), (6,6), (7,6),
    (7,0), (9,0), (9,6), (10,6), (10,7), (16,7), (16,8), (8,8)
]
RUTA_VERDE = [
    (7,12), (7,10), (6,10), (6,9), (0,9), (0,7), (6,7),
    (6,6), (7,6), (7,0), (9,0), (9,6), (10,6), (10,7),
    (16,7), (16,9), (10,9), (10,10), (9,10), (9,16),
    (8,16), (8,8)
]
RUTA_ROJO = [
    (4,7), (6,7), (6,6), (7,6), (7,0), (9,0), (9,6),
    (10,6), (10,7), (16,7), (16,9), (10,9), (10,10), (9,10),
    (9,16), (7,16), (7,10), (6,10), (6,9), (0,9),
    (0,8), (8,8)
]

RUTAS = {
    "amarillo": RUTA_AMARILLO,
    "azul": RUTA_AZUL,
    "verde": RUTA_VERDE,
    "rojo": RUTA_ROJO,
}

# ---------------------------
# CLASE FICHA
# ---------------------------
class Ficha:
    def __init__(self, color_nombre, fila, columna, indice):
        self.color_nombre = color_nombre
        self.color = COLORES_RGB[color_nombre]
        self.fila = fila
        self.columna = columna
        self.indice = indice  # 0..3
        self.en_casa = True
        self.posicion_ruta = 0
        self.actualizar_coordenadas()

    def actualizar_coordenadas(self):
        self.x = self.columna * TAM_CASILLA + OFFSET
        self.y = self.fila * TAM_CASILLA + OFFSET

    def draw(self, surface):
        """
        Dibuja la ficha como un círculo con su color
        y un texto que indica su índice + 1.
        """
        pygame.draw.circle(surface, self.color, (self.x, self.y), 15)
        fuente = pygame.font.Font(None, 24)
        texto = fuente.render(str(self.indice + 1), True, (0, 0, 0))
        surface.blit(texto, (self.x - 5, self.y - 5))

    def salir_de_casa(self):
        self.en_casa = False
        fs, cs = CASILLA_SALIDA[self.color_nombre]
        self.fila, self.columna = fs, cs
        ruta = RUTAS[self.color_nombre]
        # Buscar la casilla de salida en la ruta
        for i, (fr, fc) in enumerate(ruta):
            if (fr, fc) == (fs, cs):
                self.posicion_ruta = i
                break
        self.actualizar_coordenadas()

    def mover(self, pasos):
        """
        Avanza 'pasos' en la lista de la ruta (índice actual + pasos).
        """
        if self.en_casa:
            return
        ruta = RUTAS[self.color_nombre]
        nueva_pos = self.posicion_ruta + pasos
        if nueva_pos >= len(ruta):
            nueva_pos = len(ruta) - 1
        self.posicion_ruta = nueva_pos
        self.fila, self.columna = ruta[self.posicion_ruta]
        self.actualizar_coordenadas()

# ---------------------------
# CREAR FICHAS (4 por color)
# ---------------------------
jugadores = {}
for color in COLORES_RGB.keys():
    fichas_color = []
    for i, (fila, col) in enumerate(POSICIONES_INICIALES[color]):
        fichas_color.append(Ficha(color, fila, col, i))
    jugadores[color] = fichas_color

# ---------------------------
# FUNCIONES DIBUJAR
# ---------------------------
def pintar_cruz(surface):
    """
    Pinta la fila=8 y col=8 con CRUZ_COLOR.
    Y en (1,8), (8,16), (16,8), (8,0) con CRUZ_COLOR_FUERTE.
    """
    # Pintar fila=8
    for col in range(NUM_CASILLAS):
        if (8, col) in [(8, 0), (8, 16), (1, 8), (16, 8)]:
            color_casilla = CRUZ_COLOR_FUERTE
        else:
            color_casilla = CRUZ_COLOR
        pygame.draw.rect(
            surface, color_casilla,
            (col * TAM_CASILLA, 8 * TAM_CASILLA, TAM_CASILLA, TAM_CASILLA)
        )

    # Pintar col=8
    for fila in range(NUM_CASILLAS):
        if (fila, 8) in [(8, 0), (8, 16), (1, 8), (16, 8)]:
            color_casilla = CRUZ_COLOR_FUERTE
        else:
            color_casilla = CRUZ_COLOR
        pygame.draw.rect(
            surface, color_casilla,
            (8 * TAM_CASILLA, fila * TAM_CASILLA, TAM_CASILLA, TAM_CASILLA)
        )

def dibujar_rejilla(surface):
    surface.fill(BLANCO)
    grosor = 2
    # Primero pintamos la cruz
    pintar_cruz(surface)
    # Luego dibujamos las líneas
    for x in range(0, ANCHO + 1, TAM_CASILLA):
        pygame.draw.line(surface, NEGRO, (x, 0), (x, ALTO), grosor)
    for y in range(0, ALTO + 1, TAM_CASILLA):
        pygame.draw.line(surface, NEGRO, (0, y), (ANCHO, y), grosor)

def dibujar_casas(surface):
    # Pintamos las casas ENCIMA de la cruz
    for fila in range(0, 7):
        for col in range(0, 7):
            if (fila, col) == (6, 6):
                continue
            pygame.draw.rect(surface, (255, 200, 200),
                             (col*TAM_CASILLA, fila*TAM_CASILLA, TAM_CASILLA, TAM_CASILLA))

    for fila in range(0, 7):
        for col in range(10, 17):
            if (fila, col) == (6, 10):
                continue
            pygame.draw.rect(surface, (200, 255, 200),
                             (col*TAM_CASILLA, fila*TAM_CASILLA, TAM_CASILLA, TAM_CASILLA))

    for fila in range(10, 17):
        for col in range(10, 17):
            if (fila, col) == (10, 10):
                continue
            pygame.draw.rect(surface, (200, 200, 255),
                             (col*TAM_CASILLA, fila*TAM_CASILLA, TAM_CASILLA, TAM_CASILLA))

    for fila in range(10, 17):
        for col in range(0, 7):
            if (fila, col) == (10, 6):
                continue
            pygame.draw.rect(surface, (255, 255, 200),
                             (col*TAM_CASILLA, fila*TAM_CASILLA, TAM_CASILLA, TAM_CASILLA))

def dibujar_salidas(surface):
    for color, (fs, cs) in CASILLA_SALIDA.items():
        pygame.draw.rect(surface, MAGENTA,
                         (cs*TAM_CASILLA, fs*TAM_CASILLA, TAM_CASILLA, TAM_CASILLA))

# ---------------------------
# FUNCIÓN PARA LANZAR 2 DADOS
# ---------------------------
def lanzar_dados():
    d1 = random.randint(1, 6)
    d2 = random.randint(1, 6)
    return d1, d2

# ---------------------------
# TURNO
# ---------------------------
orden_turnos = ["rojo", "verde", "azul", "amarillo"]
turno_actual = 0
dados_lanzados = False
puede_sacar = False
d1, d2 = 0, 0

# ---------------------------
# BUCLE PRINCIPAL
# ---------------------------
running = True
while running:
    clock.tick(30)

    # 1) Dibujar el tablero (rejilla + cruz + casas + salidas)
    dibujar_rejilla(ventana)
    dibujar_casas(ventana)
    dibujar_salidas(ventana)

    # 2) Dibujar fichas (sin texto en casillas)
    for color, lista_fichas in jugadores.items():
        for ficha in lista_fichas:
            ficha.draw(ventana)

    pygame.display.flip()

    # 3) Manejo de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not dados_lanzados:
                d1, d2 = lanzar_dados()
                suma = d1 + d2
                print(f"\nTurno de {orden_turnos[turno_actual]} - Dados: {d1},{d2} => {suma}")
                if 5 in (d1, d2) or suma == 5:
                    puede_sacar = True
                    print("Puedes sacar una ficha de la casa (teclas 1-4).")
                else:
                    puede_sacar = False
                    print("No puedes sacar ficha. Mueve una que ya salió (teclas 1-4).")

                dados_lanzados = True

            elif dados_lanzados and event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]:
                index = event.key - pygame.K_1
                ficha_seleccionada = jugadores[orden_turnos[turno_actual]][index]

                if ficha_seleccionada.en_casa:
                    if puede_sacar:
                        ficha_seleccionada.salir_de_casa()
                        print(f"Sacaste la ficha {index+1} de {orden_turnos[turno_actual]}.")
                    else:
                        print(f"No puedes sacar la ficha {index+1}, no salió 5.")
                else:
                    # Mover la ficha 'suma' posiciones en su ruta
                    ficha_seleccionada.mover(d1 + d2)
                    print(f"Moviste la ficha {index+1} {d1 + d2} pasos.")

                # Pasar turno
                turno_actual = (turno_actual + 1) % len(orden_turnos)
                dados_lanzados = False
                d1, d2 = 0, 0
                puede_sacar = False

pygame.quit()
sys.exit()