import pygame
import random
import math
import time
import sys
from pygame import mixer

#  Inicializacion
pygame.init()


#Musica
musica_state = 0
mixer.music.load('background.wav')
mixer.music.play(musica_state)


#FPS
mainClock = pygame.time.Clock()
from pygame.locals import *

# Pantalla
screen = pygame.display.set_mode((1000, 800))
pygame.display.set_caption("Space Invader")
icon = pygame.image.load("spaceship.png")
pygame.display.set_icon(icon)

#Imagenes Menu
fondo_menu = pygame.image.load("fondo_menu.jpg")

boton_jugar = pygame.image.load("boton_jugar.png")
boton_salir = pygame.image.load("boton_jugar.png")

# fondo

fondo = pygame.image.load("Fondo.jpg")

# Jugador
imagen_jugador = pygame.image.load("battleship.png")
jugadorX = 360
jugadorY = 700
jugadorX_cambio = 0

# Enemigo
imagen_enemigo = []
enemigoX = []
enemigoY = []
enemigoX_cambio = []
enemigoY_cambio = []
numero_de_enemigos = 6

for x in range(numero_de_enemigos):
    imagen_enemigo.append(pygame.image.load("alien 1.png"))
    enemigoX.append(random.randint(0, 800))
    enemigoY.append(random.randint(50, 100))
    enemigoX_cambio.append(0.4)
    enemigoY_cambio.append(50)

# bala
# listo no esta en la pantalla
# fuego, esta en la pantalla
imagen_bala = pygame.image.load("Laser Listo.png")
balaX = 0
balaY = 650
balaX_cambio = 0
balaY_cambio = 1
estado_bala = "listo"

# puntuacion
puntuacion_valor = 0
font = pygame.font.Font("freesansbold.ttf", 50)
font1 = pygame.font.Font("freesansbold.ttf", 30)

textoX = 10
textoY = 10


def jugador(x, y):
    screen.blit(imagen_jugador, (x, y))


def enemigo(x, y, i):
    screen.blit(imagen_enemigo[i], (x, y))


# Disparo nave
def disparo_bala(x, y):
    global estado_bala
    estado_bala = "fuego"
    screen.blit(imagen_bala, (x + 18, y + 10))


# Colisiones
def colision(enemigoX, enemigoY, balaX, balaY):
    distancia_entre_objetos = math.sqrt(math.pow(enemigoX - balaX, 2) + math.pow(enemigoY - balaY, 2))
    if distancia_entre_objetos < 27:
        return True


# Puntuacion
def puntuacion_pantalla(x, y):
    puntuacion = font.render("Score :" + str(puntuacion_valor), True, (255, 255, 255))
    screen.blit(puntuacion, (x, y))

#Pausar el juego
def pausa():

    en_pausa = True    
    while en_pausa:
        #screen.fill((0, 0, 0))
        for evento in pygame.event.get():
            if evento.type == pygame.KEYDOWN:
                if evento.type == pygame.QUIT:
                    en_pausa = False
                    break
                if evento.key == pygame.K_ESCAPE:
                    en_pausa = False
                    break

# Fin del juego

def game_over_text():
    final = font1.render("Game Over", True, (255, 255, 255))
    screen.blit(final, (400, 400))

 
# loop del juego

#Menu inicial
#Jugar
#Opciones musica on off



def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


click = False



def main_menu():
    while True:
        # screen.fill((0, 0, 0))
        screen.blit(fondo_menu, (0, 0))
        draw_text("Space WarZone!", font, (255, 255, 255), screen, 318, 100)

        mx, my = pygame.mouse.get_pos()
        
        draw_text("Juega", font1, (255, 255, 255), screen, 468, 310)
        draw_text("Salir", font1, (255, 255, 255), screen, 475, 510) #300, 50 BOTON SIZE
        # button_1 = pygame.Rect(415, 250, 200, 50)
        button_1 = screen.blit(boton_jugar, (382, 200))
        

        button_2 = screen.blit(boton_salir, (382, 400))

        if button_1.collidepoint((mx, my)):
            if click:
                corriendo = True
                return corriendo
                break
        if button_2.collidepoint((mx, my)):
            if click:
                pygame.quit()
                sys.exit()
            

        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        mainClock.tick(60)


main_menu()
flag = False
corriendo = True
while corriendo:
    # Color del fondo en RGB
    screen.fill((0, 0, 0))
    # Cargando el fondo
    screen.blit(fondo, (0, 0))


    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False

        # Controles Movimiento y disparo
        if evento.type == pygame.KEYDOWN:
            flag = True
            if evento.key == pygame.K_LEFT:
                jugadorX_cambio = -0.6

            if evento.key == pygame.K_RIGHT:
                jugadorX_cambio = 0.6

            if evento.key == pygame.K_SPACE:
                if estado_bala == "listo":
                    balaX = jugadorX
                    disparo_bala(balaX, balaY)
            
            if evento.key == pygame.K_ESCAPE:
                pausa()

        if evento.type == pygame.KEYUP:
            if evento.key == pygame.K_RIGHT or evento.key == pygame.K_LEFT:
                jugadorX_cambio = 0


        if evento.type == pygame.K_ESCAPE:
            pausa()

    # Movimiento Jugador
    jugadorX += jugadorX_cambio

    # Margenes
    if jugadorX <= 0:
        jugadorX = 0

    elif jugadorX >= 935:
        jugadorX = 935

    # movimiento enemigo
    for i in range(numero_de_enemigos):

        # Terminar Juego
        if enemigoY[i] > 600:
            for j in range(numero_de_enemigos):
                enemigoY[j] = 2000
            game_over_text()
            break
        
        if flag:
            enemigoX[i] += enemigoX_cambio[i]
        
        if enemigoX[i] <= 0:
            enemigoX_cambio[i] = 0.9
            enemigoY[i] += enemigoY_cambio[i]
        elif enemigoX[i] >= 935:
            enemigoX_cambio[i] = -0.9
            enemigoY[i] += enemigoY_cambio[i]

        # colision entre enemigos y disparos
        colision_entre_objetos = colision(enemigoX[i], enemigoY[i], balaX, balaY)
        if colision_entre_objetos:
            balaY = 600
            estado_bala = "listo"
            puntuacion_valor += 50
            enemigoX[i] = random.randint(0, 800)
            enemigoY[i] = random.randint(50, 70)

        enemigo(enemigoX[i], enemigoY[i], i)

    # Movimiento disparos
    if balaY <= 0:
        balaY = 650
        estado_bala = "listo"

    if estado_bala == "fuego":
        disparo_bala(balaX, balaY)
        balaY -= balaY_cambio

    jugador(jugadorX, jugadorY)
    puntuacion_pantalla(textoX, textoY)
    pygame.display.update()





###########################################
#MENU


# pygame.init()
# pygame.display.set_caption('game base')
# screen = pygame.display.set_mode((500, 500), 0, 32)

# font = pygame.font.SysFont(None, 20)





# def game():
#     running = True
#     while running:
#         screen.fill((0, 0, 0))

#         draw_text('game', font, (255, 255, 255), screen, 20, 20)
#         for event in pygame.event.get():
#             if event.type == QUIT:
#                 pygame.quit()
#                 sys.exit()
#             if event.type == KEYDOWN:
#                 if event.key == K_ESCAPE:
#                     running = False

#         pygame.display.update()
#         mainClock.tick(60)


# def options():
#     running = True
#     while running:
#         screen.fill((0, 0, 0))

#         draw_text('options', font, (255, 255, 255), screen, 20, 20)
#         for event in pygame.event.get():
#             if event.type == QUIT:
#                 pygame.quit()
#                 sys.exit()
#             if event.type == KEYDOWN:
#                 if event.key == K_ESCAPE:
#                     running = False

#         pygame.display.update()
#         mainClock.tick(60)


# main_menu()