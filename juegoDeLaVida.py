import random

import pygame
import numpy as np
import time
if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Juego de la vida Marcos Gonzalez')

    # tamaño de la pantalla
    size = width, height = 1200, 900

    screen = pygame.display.set_mode(size)

    BG_COLOR = (10, 10, 10)  # Define background color
    LIVE_COLOR = (255, 255, 255)  # color celda viva
    DEAD_COLOR = (128, 128, 128)  # color celda muerta

    screen.fill(BG_COLOR)

    pygame.display.flip()

    # Tipo de texto

    fuente = pygame.font.SysFont('Arial', 25)
    numIteraciones = 0
    cantCelulas = 0
    texto1 = fuente.render("Limpiar", True, (0, 0, 0), (169, 169, 169))
    texto2 = fuente.render("Aleatorio", True, (0, 0, 0), (0, 139, 139))
    texto3 = fuente.render("Activar", True, (0, 0, 0), (0, 255, 0))
    texto4 = fuente.render("Detener", True, (255, 255, 255), (255, 0, 0))

    # Numero de celdas
    nx_Cells = 60
    ny_Cells = 60

    # Dimensiones de la celda
    dimCW = (width - 300) / nx_Cells
    dimCH = height / ny_Cells

    # Estado de las Celdas. 1 = viva, 0 = muerta
    gameState = np.zeros((nx_Cells, ny_Cells))

    # automatas predefinidos

    # automata "palo"
    gameState[5, 3] = 1
    gameState[5, 4] = 1
    gameState[5, 5] = 1

    # automata "caminante"
    gameState[21, 21] = 1
    gameState[22, 22] = 1
    gameState[22, 23] = 1
    gameState[21, 23] = 1
    gameState[20, 23] = 1

    pauseRun = True

    running = True

    # main loop
    while running:
        if(pauseRun==False):
            numIteraciones+=1

        new_gameState = np.copy(gameState)  # Copy status
        cantCelulas=0
        for x in range(nx_Cells):
            for y in range(ny_Cells):
                if new_gameState[x, y] == 1:
                    cantCelulas += 1


        # detectamos los eventos
        for event in pygame.event.get():

            if event.type == pygame.QUIT:  # se cierra la pantalla
                running = False  # cerramos el juego

            if event.type == pygame.KEYDOWN:  # se presiona una tecla
                pauseRun = not pauseRun  # pausamos el juego

            mouseClick = pygame.mouse.get_pressed()  # presionamos un boton del muse
            if sum(mouseClick) > 0:
                try:
                    posX, posY = pygame.mouse.get_pos()  # obtenemos la posicion del cursor en ese momento
                    # Función para vaciar la matriz
                    if 1000 <= posX < 1100 and 50 <= posY < 90:
                        new_gameState = np.copy(np.zeros((nx_Cells, ny_Cells)))
                        numIteraciones=0
                        cantCelulas=0
                        pauseRun = True
                    # Función para generar una matriz aleatoria
                    if 1000 <= posX < 1100 and 150 <= posY < 190:
                        pauseRun = True
                        numIteraciones=0
                        cantCelulas=0
                        for x in range(nx_Cells):
                            for y in range(ny_Cells):
                                new_gameState[x, y] = random.randint(0, 1)
                    # Función para activar
                    if 1000 <= posX < 1100 and 250 <= posY < 290:
                        pauseRun = not pauseRun
                    x, y = int(np.floor(posX / dimCW)), int(np.floor(posY / dimCH))  # ubicamos la celda señalada
                    new_gameState[x, y] = not mouseClick[2]  # asignamos el estado a la celda (btn der: muere; btn izq: vive)
                except:
                    print(mouseClick)

        screen.fill(BG_COLOR)
        for y in range(0, ny_Cells):
            for x in range(0, nx_Cells):
                if not pauseRun:
                    # Calculo de vecinos cercanos
                    n_neigh = gameState[(x - 1) % nx_Cells, (y - 1) % ny_Cells] + \
                              gameState[(x) % nx_Cells, (y - 1) % ny_Cells] + \
                              gameState[(x + 1) % nx_Cells, (y - 1) % ny_Cells] + \
                              gameState[(x - 1) % nx_Cells, (y) % ny_Cells] + \
                              gameState[(x + 1) % nx_Cells, (y) % ny_Cells] + \
                              gameState[(x - 1) % nx_Cells, (y + 1) % ny_Cells] + \
                              gameState[(x) % nx_Cells, (y + 1) % ny_Cells] + \
                              gameState[(x + 1) % nx_Cells, (y + 1) % ny_Cells]

                    # Rule 1: Una celula muerta con 3 vecinas revive
                    if gameState[x, y] == 0 and n_neigh == 3:
                        new_gameState[x, y] = 1
                    # Rule 2: Una celula viva con mas de 3 o menos de 2 vecinos vivos muere
                    elif gameState[x, y] == 1 and (n_neigh < 2 or n_neigh > 3):
                        new_gameState[x, y] = 0

                # Poligno para cada celda a dibujar
                poly = [
                    ((x) * dimCW, (y) * dimCH),
                    ((x + 1) * dimCW, (y) * dimCH),
                    ((x + 1) * dimCW, (y + 1) * dimCH),
                    ((x) * dimCW, (y + 1) * dimCH)
                ]

                # Dibujamos en cada celda
                if new_gameState[x, y] == 0:
                    pygame.draw.polygon(screen, DEAD_COLOR, poly, 1)
                else:
                    pygame.draw.polygon(screen, LIVE_COLOR, poly, 0)


        gameState = np.copy(new_gameState)
        time.sleep(0.02)
        pygame.draw.rect(screen, (169, 169, 169), (1000, 50, 100, 40))
        screen.blit(texto1, (1015, 55, 100, 40))
        pygame.draw.rect(screen, (0, 139, 139), (1000, 150, 100, 40))
        screen.blit(texto2, (1010, 155, 100, 40))
        pygame.draw.rect(screen, (0, 255, 0), (1000, 250, 100, 40))
        screen.blit(texto3, (1010, 255, 100, 40))
        if(pauseRun == False):
            pygame.draw.rect(screen, (255, 0, 0), (1000, 250, 100, 40))
            screen.blit(texto4, (1010, 255, 100, 40))

        iteraciones = fuente.render("Iteración número: " + str(numIteraciones), True, (255, 255, 255), (0, 0, 0))
        screen.blit(iteraciones, (930, 500, 100, 40))
        cantidad = fuente.render("Células vivas: " + str(cantCelulas), True, (255, 255, 255), (0, 0, 0))
        screen.blit(cantidad, (930, 550, 100, 40))
        pygame.display.flip()