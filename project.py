import pygame 
from random import randint

pygame.init()
# Crear la ventana del juego con dimensiones 640x480 píxeles
ventana = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Zagal_Manero")

# -------------------------------
# Cargar y escalar la imagen de la pelota
# -------------------------------
ball = pygame.image.load("ball.png")
# Redimensionar la pelota a 20x20 píxeles (tamaño estándar y no muy grande)
ball = pygame.transform.scale(ball, (20, 20))
ballrect = ball.get_rect()  # Obtener el rectángulo delimitador de la pelota
speed = [randint(3, 6), randint(3, 6)]  # Asignar velocidades aleatorias en x e y
ballrect.move_ip(0, 0)  # Posicionar la pelota (sin desplazarla)

# -------------------------------
# Cargar y escalar la imagen del bate (barra)
# -------------------------------
barra = pygame.image.load("barra.png")
# Redimensionar el bate a 100x15 píxeles (tamaño estándar)
barra = pygame.transform.scale(barra, (100, 15))
barrarect = barra.get_rect()  # Obtener el rectángulo delimitador del bate
barrarect.move_ip(240, 450)  # Posicionar el bate en la ventana

# Fuente para mostrar mensajes (por ejemplo, "Game Over")
fuente = pygame.font.Font(None, 36)

# Variable para controlar el bucle principal del juego
jugando = True
while jugando:
    # Manejo de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            jugando = False

    # Movimiento del bate con las teclas izquierda y derecha
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        barrarect = barrarect.move(-3, 0)  # Mover el bate a la izquierda
    if keys[pygame.K_RIGHT]:
        barrarect = barrarect.move(3, 0)   # Mover el bate a la derecha

    # Detección de colisión entre el bate y la pelota para rebotar la pelota
    if barrarect.colliderect(ballrect):
        speed[1] = -speed[1]  # Invertir la dirección vertical de la pelota

    # Actualizar la posición de la pelota
    ballrect = ballrect.move(speed)

    # Rebotar la pelota al chocar con los bordes laterales
    if ballrect.left < 0 or ballrect.right > ventana.get_width():
        speed[0] = -speed[0]
    # Rebotar la pelota al chocar con el borde superior
    if ballrect.top < 0:
        speed[1] = -speed[1]
    
    # Comprobar si la pelota ha salido por el borde inferior (Game Over)
    if ballrect.bottom > ventana.get_height():
        # Renderizar el mensaje de "Game Over"
        texto = fuente.render("Game Over", True, (125, 125, 125))
        texto_rect = texto.get_rect()
        texto_x = ventana.get_width() / 2 - texto_rect.width / 2
        texto_y = ventana.get_height() / 2 - texto_rect.height / 2
        ventana.blit(texto, [texto_x, texto_y])
    else:
        # Rellenar la ventana con un color de fondo claro
        ventana.fill((252, 243, 207))
        # Dibujar la pelota y el bate en la ventana
        ventana.blit(ball, ballrect)
        ventana.blit(barra, barrarect)

    # Actualizar la pantalla para mostrar los cambios
    pygame.display.flip()
    # Controlar la tasa de refresco (60 FPS)
    pygame.time.Clock().tick(60)

pygame.quit()
