import pygame
import math
import time
from copy import deepcopy


class GameOfLife:

    def __init__(self, size):
        self.size = size
        self.pausa = True
        self.tablero = [[0 for _ in range(size)] for _ in range(size)]

    # Metodo especial para imprimir un objeto
    def __str__(self):
        resultado = ""
        for i in range(len(self.tablero)):
            for j in range(len(self.tablero[i])):
                resultado += str(self.tablero[i][j]) + " "
            resultado += "\n"
        return resultado

    # Los metodos privados se denotan con __ al principio
    def revisar_vecinos(self, i, j):
        numero_vecinos = 0
        mov_x = [-1, -1, -1, 0, 0, 1, 1, 1]
        mov_y = [-1, 0, 1, -1, 1, -1, 0, 1]
        for k in range(len(mov_x)):
            if len(self.tablero) > i + mov_x[k] >= 0 and len(self.tablero[0]) > j + mov_y[k] >= 0:
                if self.tablero[i + mov_x[k]][j + mov_y[k]] == 1:
                    numero_vecinos += 1
        return numero_vecinos

    def run(self):
        nuevo_tablero = [[0 for _ in range(self.size)] for _ in range(self.size)]
        for i in range(self.size):
            for j in range(self.size):
                if self.tablero[i][j] == 1 and (self.revisar_vecinos(i, j) < 2 or self.revisar_vecinos(i, j) > 3):
                    nuevo_tablero[i][j] = 0
                elif self.tablero[i][j] == 1 and (self.revisar_vecinos(i, j) == 2 or self.revisar_vecinos(i, j) == 3):
                    nuevo_tablero[i][j] = 1
                elif self.tablero[i][j] == 0 and (self.revisar_vecinos(i, j) == 3):
                    nuevo_tablero[i][j] = 1
        self.tablero = deepcopy(nuevo_tablero)


def dibujar_tablero(game, surf, width, height):
    # Se configura el color de los rectangulos
    blanco = (255, 255, 255)
    gris = (71, 66, 66)
    # Se definen los deltas
    dx = 0
    dy = 0
    # Se dibujan las celdas
    for i in range(game.size):
        for j in range(game.size):
            if j != 0:
                dx += width / game.size
            if game.tablero[i][j] == 1:
                pygame.draw.rect(surf, blanco, pygame.Rect(dx, dy, width / game.size, height / game.size))
            else:
                pygame.draw.rect(surf, gris, pygame.Rect(dx, dy, width / game.size, height / game.size), 1)
        dx = 0
        dy += height / game.size


def main():
    dim_juego = 10
    juego = GameOfLife(dim_juego)
    pygame.init()
    clock = pygame.time.Clock()
    # Se definen las dimensiones de la pantalla
    ancho = 650
    alto = 650
    # Se configura el icono de la ventana
    icon = pygame.image.load("img/icon.png")
    pygame.display.set_icon(icon)
    # Se establece el titulo de la ventana
    pygame.display.set_caption("Game of life - En pausa")
    run = False
    while True:
        # Se guarda en una variable el objeto de la pantalla
        surface = pygame.display.set_mode((ancho, alto))
        # Revisa los eventos que ocurren durante la ejecucion del programa
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()  # Hace que el sistema salga
                exit()  # Cierra la ventana
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                cel_x = math.floor(x / (ancho / dim_juego))
                cel_y = math.floor(y / (alto / dim_juego))
                juego.tablero[cel_y][cel_x] = 0 if juego.tablero[cel_y][cel_x] == 1 else 1
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                run = not run
                if run is True:
                    pygame.display.set_caption("Game of life - En juego")
                else:
                    pygame.display.set_caption("Game of life - En pausa")
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                run = False
                pygame.display.set_caption("Game of life - Juego reiniciado")
                juego = GameOfLife(dim_juego)
        if run:
            juego.run()
        dibujar_tablero(juego, surface, ancho, alto)
        time.sleep(0.1)
        # Esta funcion se usa para actualizar el contenido de la pantalla
        pygame.display.flip()
        clock.tick(20)


if __name__ == "__main__":
    main()
