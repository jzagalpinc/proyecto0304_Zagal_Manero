import pygame 
from random import randint

#----------------------------------------------------------
# CREAMOS LA VENTANA
pygame.init()
ventana = pygame.display.set_mode((640, 480)) #crear la ventana del juego con dimensiones 640x480 píxeles
pygame.display.set_caption("Zagal_Manero")

#----------------------------------------------------------
# AÑADIMOS LA PELOTA
ball = pygame.image.load("ball.png") #cargamos la imagen de la pelota
ball = pygame.transform.scale(ball, (20, 20)) #redimensionamos la pelota 
ballrect = ball.get_rect() #marcar el cuadrado delimitador de la pelota
speed = [randint(3, 6), randint(3, 6)]  #asignar velocidades aleatorias en x e y
ballrect.move_ip(0, 0)  #posicionar la pelota

#--------------------------------------------------------
# AÑADIMOS LA BARRA
barra = pygame.image.load("barra.png") #cargamos la imagen de la barra
barra = pygame.transform.scale(barra, (100, 15)) #redimensionamos la barra
barrarect = barra.get_rect()  #obtener el rectángulo delimitador la barra
barrarect.move_ip(240, 450)  #posicionamos el bate en la ventana

#--------------------------------------------------------
# AÑADIMOS LA FUENTE DE LA LETRA
fuente = pygame.font.Font(None, 36) #fuente para mosTrar mensajes

#--------------------------------------------------------
# VELOCIDADES DE LA BARRA
velocidad_barra = 3  #velocidad inicial de la barra
aceleracion = 0.2  #aumento progresivo de velocidad de la barra
velocidad_maxima = 8  #limite superior de velocidad de la barra

#---------------------------------------------------------
# AUMENTO DE LA VELOCIDAD DE LA PELOTA
rebotes = 0 #variable para conar el numero de rebotes en la barra
incremento_velocidad = 0.5 #cantidad de aumento de velocidad cada ciertos revotes
rebotes_para_acelerar = 5 #numero de reboes para aumentar la velocidad

#----------------------------------------------------------
# CREAMOS LA CLASE LADRILLO
class Ladrillo:
    def __init__(self, x, y, color):
        self.rect = pygame.Rect(x, y, 60, 20) #definimos el rectangulo del ladrillo
        self.color = color #color del ladrillo
        self.estado = True #activo o destruido (True=no destruido)
    
    def dibujar (self, ventana):
        if self.estado: #si el ladrillo no esta destruido lo dibujamos
            pygame.draw.rect(ventana, self.color, self.rect)
    
    def destruir (self):
        self.estado = False #cambiamos el estado a desruido

    def colision(self, pelota):
        if self.estado: #si el ladrillo no esta destruido
            if self.rect.colliderect(pelota):
                self.destruir() #destruimos el ladrillo
                return True
        return False

#----------------------------------------------------------
# CREAMOS HERENCIA DE LADRILLO PARA LADRILLOIRROMPIBLE
class LadrilloIrrompible(Ladrillo):
    def __init__(self, x, y, color):
        super().__init__(x, y, color) #llamamos al constructor de la clase
        self.estado = True #ladrillo irrompible
    
    def colision(self, pelota): #en estta clase no se destrulle el ladrillo
        if self.estado:
            if self.rect.colliderect(pelota):
                return True #el ladrillo se toca pero no se destrulle
        return False

#----------------------------------------------------------
# CREAMOS LOS LADRILLOS
ladrillo1 = Ladrillo (270, 100, (0,0,255)) #ladrillo normal
ladrillo2 = LadrilloIrrompible (200,100, (0,255,0)) #ladrillo irrompible

#----------------------------------------------------------
# CRONTROLAR EL JUEGO
jugando = True
while jugando:

    # Manejo de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #si el usuario cierra la venttana
            jugando = False #terminamos el bucle y cerramos el juego

    # Movimiento del bate con las teclas izquierda y derecha mas aceleracion
    keys = pygame.key.get_pressed() #obtenemos las teclas
    if keys[pygame.K_LEFT]: #al presionar la tecla izquierda
        velocidad_barra = min(velocidad_barra + aceleracion, velocidad_maxima) #aumenta la velocidad
        barrarect.x = max(0, barrarect.x - int(velocidad_barra))  # mueve la barra y evita que la barra salga por la izquierda 

    elif keys[pygame.K_RIGHT]: #al presionar la tecla derecha
        velocidad_barra = min(velocidad_barra + aceleracion, velocidad_maxima)  #amenta la velocidad
        barrarect.x = min(ventana.get_width() - barrarect.width, barrarect.x + int(velocidad_barra)) #mueve la barra y evita que la barra salga por la derecha

    else:
        velocidad_barra = max(3, velocidad_barra - aceleracion) #desaceleracion al no pulsar la barra

    # Detección de colisión entre el bate y la pelota para rebotar la pelota y cambio de angulo
    if barrarect.colliderect(ballrect): #si la pelota toca la barra
        impacto = (ballrect.centerx - barrarect.centerx) / (barrarect.width / 2) #calculamos la posicion relativa del impacto en la barra
        speed[1] = -speed[1] #invertimos la direccion en y en rebote normal
        speed[0] += int(impacto * 2)  #modificamos la direccion en X segun el impacto
        if speed[0] == 0: #evitamos el rebote recto
            speed[0] = 1 if impacto > 0 else -1 #le damos un movimiento para dar movimiento
        rebotes +=1 #aumentamos el numero de rebotes
        if rebotes % rebotes_para_acelerar == 0: #aceleracion de la pelota cuando se llega al numero de rebotes
            speed [0] *= 1 + incremento_velocidad #aumentamos velocidad en eje X
            speed [1] *= 1 + incremento_velocidad #aumentamos velocidad en eje Y

    # Actualizar la posición de la pelota
    ballrect = ballrect.move(speed)

    # Rebotar la pelota al chocar con los bordes laterales
    if ballrect.left < 0 or ballrect.right > ventana.get_width(): #si la pelota toca el borde izquierdo o derecho
        speed[0] = -speed[0] #cambiamos la direccion X para que rebote

    # Rebotar la pelota al chocar con el borde superior
    if ballrect.top < 0: #cuando la pelota toca el borde superior
        speed[1] = -speed[1] # cambiamos la direccion Y para que rebote
     
    # Comprobar si la pelota ha salido por el borde inferior y Game Over
    if ballrect.bottom > ventana.get_height(): #si la pelota sale por abajo
        texto = fuente.render("Game Over", True, (125, 125, 125)) #creamos el mesaje
        texto_rect = texto.get_rect() #obttenemos rectangulo para centrar el texto
        texto_x = ventana.get_width() / 2 - texto_rect.width / 2 #lo centramos en X
        texto_y = ventana.get_height() / 2 - texto_rect.height / 2 #lo cenramos en Y
        ventana.blit(texto, [texto_x, texto_y]) #mosramos el mensaje en la pantalla
    else: #si el juego no ha terminado 
        ventana.fill((252, 243, 207)) #llenamos la ventana con color
        ventana.blit(ball, ballrect) #dibujamos la pelota
        ventana.blit(barra, barrarect) #dibujamos la barra

    # Dibujamos los ladrillos
    ladrillo1.dibujar(ventana)
    ladrillo2.dibujar(ventana)

    # Verificamos si la pelota choca con el ladrillo
    if ladrillo1.colision(ballrect): #comprobamos la colision con el ladrillo
        speed[1] = -speed[1] #la pelota rebota

    if ladrillo2.colision(ballrect): #comprobamos la colision con el ladrillo irrompible
        speed[1] = -speed[1] #la pelota rebota
        
    # Actualizar la pantalla para mostrar los cambios
    pygame.display.flip()

    # Controlar la tasa de refresco (60 FPS)
    pygame.time.Clock().tick(60)

pygame.quit()
