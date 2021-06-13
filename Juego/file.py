import pygame 
from pygame import mixer

pygame.init()

musica_state = 0
mixer.music.load('background.wav')
mixer.music.play(musica_state)

screen = pygame.display.set_mode((1000, 800))
fondo = pygame.image.load("Fondo.jpg")
corriendo = True
while corriendo:
    # Color del fondo en RGB
    screen.fill((0, 0, 0))
    # Cargando el fondo
    screen.blit(fondo, (0, 0))

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_RETURN:
                mixer.music.stop()
            if evento.key == pygame.K_SPACE:
                mixer.music.play(musica_state)
