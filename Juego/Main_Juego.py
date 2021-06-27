import pygame
import random
import math
import time
import sys
from pygame import mixer

#  Inicializacion del pygame
pygame.init()


# Iniciar la musica de fonto
musica_state = -1
musica = True
mixer.music.load('background.wav')
mixer.music.play(musica_state)


#Fotogramas por segundo
mainClock = pygame.time.Clock()
from pygame.locals import *

# Pantalla
screen = pygame.display.set_mode((1000, 800))
pygame.display.set_caption("Space Invader")
icon = pygame.image.load("spaceship.png")
pygame.display.set_icon(icon)

#Imagenes Menu
fondo_menu = pygame.image.load("fondo_menu.jpg")

boton_jugar = pygame.image.load("boton_jugar_new.png")
boton_opciones = pygame.image.load("boton_jugar_new.png")
boton_salir = pygame.image.load("boton_jugar_new.png")
boton_volver = pygame.image.load("boton_jugar_new.png")
boton_mon = pygame.image.load("boton_jugar_new.png")
boton_moff = pygame.image.load("boton_jugar_new.png")

#Bonifiaciones
power_up_bala = pygame.image.load("pu_bala.png")
flag1 = True
hay_bonificador = False
bonificacionY = 0
bonificionY_cambio = 0.5

# Fondo del juego
fondo = pygame.image.load("Fondo.jpg")

# Variables del jugador: posicion y sprite
imagen_jugador = pygame.image.load("battleship.png")
jugadorX = 445
jugadorY = 700
jugadorX_cambio = 0

# Variables del enemigo: cantidad maxima en un mismo momento y sprite.
imagen_enemigo = []
enemigoX = []
enemigoY = []
enemigoX_cambio = []
enemigoY_cambio = []
numero_de_enemigos = 6

#Colocar a los enemigos en partes aleatorias dentro de la pantalla
for x in range(numero_de_enemigos):
    imagen_enemigo.append(pygame.image.load("alien 1.png"))
    enemigoX.append(random.randint(0, 800))
    enemigoY.append(random.randint(50, 100))
    enemigoX_cambio.append(0.4)
    enemigoY_cambio.append(50)

# Bala
# Listo no esta en la pantalla
# Fuego, esta en la pantalla
imagen_bala = pygame.image.load("Laser Listo.png")
balaX = 0
balaY = 650
balaX_cambio = 0
balaY_cambio = 1
estado_bala = "listo"
contador_bala = []
max_balas = 3
bonificacion_bala = 1

# Poner la puntuacion en 0 cuando inicia el juego
puntuacion_valor = 0
font = pygame.font.Font("freesansbold.ttf", 50)
font1 = pygame.font.Font("freesansbold.ttf", 30)

textoX = 10
textoY = 10

# Colocar al jugador en X, Y correspondientes 
def jugador(x, y):
    screen.blit(imagen_jugador, (x, y))

# Colocar a los enemigos donde corresponda
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

#Pausar el juego.
def pausa():

    en_pausa = True    
    while en_pausa:
        for evento in pygame.event.get():
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    en_pausa = False
                    break
            if evento.type == pygame.QUIT:
                quit()


# Fin del juego.
def game_over_text():
    final = font1.render("Game Over", True, (255, 255, 255))
    screen.blit(final, (400, 400))

#Menu opciones
def menu_opciones(musica):
    while True:
        screen.blit(fondo_menu, (0, 0))
        dibujar_texto("Opciones", font, (255, 255, 255), screen, 393, 100)

        # Obtener la posicion del mouse
        mx, my = pygame.mouse.get_pos()

        dibujar_texto("Musica ON", font1, (255, 255, 255), screen, 285, 300)
        dibujar_texto("Musica OFF", font1, (255, 255, 255), screen, 560, 300)
        dibujar_texto("Volver", font1, (255, 255, 255), screen, 475, 510)

        button_1 = screen.blit(boton_mon, (230, 288))     
        button_2 = screen.blit(boton_moff, (520, 288))
        button_3 = screen.blit(boton_volver, (388, 497))
        
        if button_1.collidepoint((mx, my)):
            if click and musica == False:
                musica = True
                mixer.music.play(-1)

        if button_2.collidepoint((mx, my)):
            if click and musica == True:
                musica = False
                mixer.music.stop()

        if button_3.collidepoint((mx, my)):
            if click:
                return musica
        
        click = False

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        
        #print(musica)
        pygame.display.update()
        mainClock.tick(60)

# Funcion que crea un texto dado ciertas variables.
# Reutilizable.
def dibujar_texto(text, font, color, superficie, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    superficie.blit(textobj, textrect)

def bonificacion(posicionX, bonificacionY):
    screen.blit(power_up_bala, (posicionX, bonificacionY))


click = False


# Funcion del menu principal
def main_menu(musica):
    while True:
        
        # Dibujar la imagen de fondo y el texto "Space WarZone!"
        screen.blit(fondo_menu, (0, 0))
        dibujar_texto("Space WarZone!", font, (255, 255, 255), screen, 318, 100)

        # Obtener la posicion del mouse
        mx, my = pygame.mouse.get_pos()
        
        # Dibujar el texto "Jugar" y "Salir" en donde corresponde
        dibujar_texto("Juega", font1, (255, 255, 255), screen, 468, 310)
        dibujar_texto("Opciones", font1, (255, 255, 255), screen, 444, 412)
        dibujar_texto("Salir", font1, (255, 255, 255), screen, 475, 510)
        

        #Dibujar los botones en donde corresponde
        button_1 = screen.blit(boton_jugar, (382, 300))     
        button_2 = screen.blit(boton_salir, (382, 500))
        button_3 = screen.blit(boton_opciones, (382, 400))

        # Si el usuario clickea en el boton "Jugar" entonces incie el juego.
        if button_1.collidepoint((mx, my)):
            if click:
                corriendo = True
                return corriendo

        # Si el usuario clickea en el boton "Salir" salga del programa.
        if button_2.collidepoint((mx, my)):
            if click:
                pygame.quit()
                sys.exit()
        
        if button_3.collidepoint((mx, my)):
            if click:
                musica = menu_opciones(musica)
            
        # Manejar la mecanica del "click izquirdo"
        click = False

        # Si el usuario apreta la "X" de arriba a la derecha entonces salga del programa
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            
            # Si el usuario apreta la tecla "escape" entonces salga del programa.
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            
            # Si el usuario hace "click izquierdo" entonces la variable "click" es igual a True.
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        #print(musica)
        # Actualizar la pantalla cada 60 FPS.
        pygame.display.update()
        mainClock.tick(60)

# Llamar a la funcion "main_menu".
main_menu(musica)

# Un "flag" para poder manejar el inicio del juego.
flag = False

# Inicie el juego.
corriendo = True
while corriendo:
    # Color del fondo en RGB
    screen.fill((0, 0, 0))
    # Cargando el fondo
    screen.blit(fondo, (0, 0))


    #Si flag es False entonces dibuje el texto "Pulse una telca para continuar".
    if flag == False:
        dibujar_texto("Pulse una tecla para jugar!", font, (255, 255, 255), screen, 170, 500)

    # Manejar los eventos y las teclas pulsadas por el jugador
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False

        # Controles Movimiento y disparo
        # Si el jugador a pulsado cualquier tecla, entonces inicie el movimiento de los enemigos
        if evento.type == pygame.KEYDOWN:
            flag = True
            if evento.key == pygame.K_LEFT:
                jugadorX_cambio = -0.6

            if evento.key == pygame.K_RIGHT:
                jugadorX_cambio = 0.6

            if evento.key == pygame.K_SPACE:
                if estado_bala == "listo":
                    balaX = jugadorX
                    contador_bala.append(1)
                    disparo_bala(balaX, balaY)
                


            
            # Pause el juego si el jugador presiono la tecla "escape".
            # Reanudar el juego si se presiona la tecla "escape" nuevamente.
            if evento.key == pygame.K_ESCAPE:
                pausa()

        # Manejar al movimiento del jugador.
        if evento.type == pygame.KEYUP:
            if evento.key == pygame.K_RIGHT or evento.key == pygame.K_LEFT:
                jugadorX_cambio = 0

        # Manejar la pausa del juego.
        if evento.type == pygame.K_ESCAPE:
            pausa()

    # Movimiento Jugador
    jugadorX += jugadorX_cambio

    # Margenes
    if jugadorX <= 0:
        jugadorX = 0

    elif jugadorX >= 935:
        jugadorX = 935

    # Movimiento enemigo
    for i in range(numero_de_enemigos):

        # Terminar el juego si el enemigo llego a la posicion (x, 600)
        if enemigoY[i] > 600:
            for j in range(numero_de_enemigos):
                enemigoY[j] = 2000
            game_over_text()
            break
        
        # Si flag es True entonces los enemigos se moveran
        if flag:
            enemigoX[i] += enemigoX_cambio[i]
        
        if enemigoX[i] <= 0:
            enemigoX_cambio[i] = 0.9
            enemigoY[i] += enemigoY_cambio[i]
        elif enemigoX[i] >= 935:
            enemigoX_cambio[i] = -0.9
            enemigoY[i] += enemigoY_cambio[i]

        # Colision entre enemigos y disparos
        colision_entre_objetos = colision(enemigoX[i], enemigoY[i], balaX, balaY)
        if colision_entre_objetos:
            balaY = 600
            estado_bala = "listo"
            puntuacion_valor += 50
            enemigoX[i] = random.randint(0, 800)
            enemigoY[i] = random.randint(50, 70)

        enemigo(enemigoX[i], enemigoY[i], i)


    #Generar bonificacion de bala.
    numero_random = random.randint(1, 10000)
    if numero_random == 2:  #and puntuacion_valor > 100:
        hay_bonificador = True
    if hay_bonificador:
        if flag1:
            posicionX = random.randint(0, 800)
            flag1 = False
        bonificacionY += bonificionY_cambio
        bonificacion(posicionX, bonificacionY)
    if bonificacionY >= 1000:
        flag1 = True
        hay_bonificador = False
        bonificacionY = 0




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