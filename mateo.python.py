import pygame
import random

#CONSTANTES
ANCHO = 1200
ALTO = 600

VERDE = (0, 255, 0)
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)

#INICIADOR DE JUEGO
pygame.init()
pygame.mixer.init()

#PANTALLA 
screen = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Galaxia")
clock = pygame.time.Clock()

#FUNCION PARA DIBUJAR TEXTO
def dibujar_texto(surface, text, size, x, y):
    font = pygame.font.SysFont("serif", size)
    text_surface = font.render(text, True, BLANCO)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)


#FUNCION PARA DIBUJAR BARRA SALUD
def dibujar_barra_salud(surface, x, y, percentage):
    BAR_LENGTH = 150
    BAR_HEIGHT = 10
    fill = (percentage / 100) * BAR_LENGTH
    border = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surface, VERDE, fill)
    pygame.draw.rect(surface, BLANCO, border, 2)


# CLASES
class Proyectil(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("disparo.png")
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.image.set_colorkey(NEGRO)
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.centerx = x
        self.speedy = -10

    #desplaza el proyectil y lo elimina si supera la parte superior
    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()


class Jugador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("nave1.png").convert()
        self.image.set_colorkey(NEGRO)
        self.rect = self.image.get_rect()
        self.rect.centerx = ANCHO // 2
        self.rect.bottom = ALTO - 10
        self.speed_x = 0
        self.shield = 100

    #Permite el movimiento y delimita para que no salga de la pantalla
    def update(self):
        self.speed_x = 0
        keystate = pygame.key.get_pressed()

        if keystate[pygame.K_LEFT]:
            self.speed_x = -5
        if keystate[pygame.K_RIGHT]:
            self.speed_x = 5
        self.rect.x += self.speed_x

        if self.rect.right > ANCHO:
            self.rect.right = ANCHO
        if self.rect.left < 0:
            self.rect.left = 0

    #Crea el proyectil en la posicion del jugador y lo agrega a grupos de sprite y reproduce sonido
    def shoot(self):
        bullet = Proyectil(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
        laser_sound.play()


class Meteoro(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = random.choice(meteor_imagenes)
        self.image.set_colorkey(NEGRO)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(ANCHO - self.rect.width)
        self.rect.y = random.randrange(-140, -100)
        self.speedy = random.randrange(1, 10)
        self.speedx = random.randrange(-5, 5)

    #Actualiza la posicion del meteoro y si se sale de pantalla lo vuelve a generar
    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > ALTO + 10 or self.rect.left < -100 or self.rect.right > ANCHO + 100:
            self.rect.x = random.randrange(ANCHO - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 10)

    #Crea una explosion en la posicion del meteoro y agrega a los grupos correspondientes
    def explode(self):
        explosion = Explosion(self.rect.center)
        all_sprites.add(explosion)
        explosions.add(explosion)


class Explosion(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.image = pygame.image.load("explosion1.png")
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.frame = 0
        self.animation = 10

    #Actualiza la animacion de la explocion y la elimina cuando se completa
    def update(self):
        self.frame += 1
        if self.frame == self.animation:
            self.kill()

#PANTALLA DE INICIO
def Pantalla_inicio():
    dibujar_texto(screen, "LLUVIA DE METEORITOS", 65, ANCHO // 2, ALTO // 4)
    dibujar_texto(screen, "Tu objetivo es destruir el mayor número de meteoritos. Solo podrás recibir 4 impactos.", 27,ANCHO // 2, ALTO // 2)
    dibujar_texto(screen, "Presiona cualquier tecla para jugar", 20, ANCHO // 2, ALTO * 3 / 4)
    pygame.display.flip()
    #Espera que se toque una tecla para salir o que se cierre el juego
    waiting = True
    while waiting:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False

#PANTALLA DE GAME OVER
def Pantalla_game_over(score,tiempo_final):
    screen.fill(NEGRO)
    dibujar_texto(screen, "Juego Terminado.", 65, ANCHO // 2, ALTO // 4)
    dibujar_texto(screen, "Tu nave fue destruida", 45, ANCHO // 2, ALTO // 2.5)
    dibujar_texto(screen,f"Puntaje obtenido: {score}",27,ANCHO//2,ALTO//2)
    dibujar_texto(screen, f"Tiempo de juego: {tiempo_final //60}", 27, ANCHO // 2, ALTO // 1.8) 
    dibujar_texto(screen, "Presiona cualquier tecla para volver a jugar", 27, ANCHO // 2, ALTO // 1.5)
    pygame.display.flip()

#Reinicia el juego, elimina todos los sprites, crea 10 meteoros y retorna un jugador
def reiniciar_juego():
    all_sprites.empty()
    meteors.empty()
    bullets.empty()
    explosions.empty()

    jugador = Jugador()
    all_sprites.add(jugador)

    for i in range(6):
        meteoro = Meteoro()
        all_sprites.add(meteoro)
        meteors.add(meteoro)
    return jugador

#CARGAR IMAGENES METEOROS
meteor_imagenes = []
meteor_list = [
    "astteroide.png",
    "astteroide1.png",
    "astteroide2.png",
]

for img in meteor_list:
    meteor_imagenes.append(pygame.image.load(img).convert())

#ESTABLECER FONDO DE PANTALLA
background = pygame.image.load("fondo_pantalla.jpg").convert()

# SONIDOS
laser_sound = pygame.mixer.Sound("laser5.ogg")
explosion_sound = pygame.mixer.Sound("explosion.wav")
musica_fondo = pygame.mixer.Sound("musica_juego.mp3")
pygame.mixer.music.set_volume(0.2)
musica_fondo.play(-1)

#SPRITES
all_sprites = pygame.sprite.Group()#se crea el grupo de todos los sprites
meteors = pygame.sprite.Group()# grupo para almacenar los meteoros
bullets = pygame.sprite.Group()# grupo para alacenar los sprites de las balas
explosions = pygame.sprite.Group()# grupo para almacenar los sprites de las explosiones
jugador = Jugador()#se crea instancia de jugador
all_sprites.add(jugador)#se agrega al grupo all_sprites

#CREACION DE LOS PRIMEROS METEOROS
for i in range(6):
    meteoro = Meteoro()
    all_sprites.add(meteoro)
    meteors.add(meteoro)

# PANTALLA DE INICIO
Pantalla_inicio()

#VARIABLES
tiempo= 0
score = 0
nivel = 1
running = True
game_over = False

#BUCLE WHILE
while running:
    tiempo += 1
    clock.tick(60)
    if game_over:
        Pantalla_game_over(score,tiempo_final )
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYUP:
                jugador = reiniciar_juego()
                game_over = False
                score = 0
                nivel = 1
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    jugador.shoot()

        all_sprites.update()

        # Colisión del proyectil con el meteoro
        hits = pygame.sprite.groupcollide(meteors, bullets, True, True)
        for hit in hits:
            score += 1
            hit.explode()
            explosion_sound.play()
            meteoro = Meteoro()
            all_sprites.add(meteoro)
            meteors.add(meteoro)

        # Colisión del jugador con el meteoro
        hits = pygame.sprite.spritecollide(jugador, meteors, True)
        for hit in hits:
            jugador.shield -= 25
            meteoro = Meteoro()
            all_sprites.add(meteoro)
            meteors.add(meteoro)
            if jugador.shield <= 0:
                game_over = True
                tiempo_final = tiempo
                tiempo= 0    
        screen.blit(background, [0, 0])

        all_sprites.draw(screen)

        # Barra de salud
        dibujar_texto(screen, "Salud de la nave", 20, 80, 18)
        dibujar_barra_salud(screen, 5, 5, jugador.shield)

        # Puntaje
        dibujar_texto(screen, f"Puntaje: {score}", 20, ANCHO // 2, 10)

        # Nivel
        dibujar_texto(screen, f"Nivel: {nivel}", 20, ANCHO - 50, 10)

        pygame.display.flip()

        # Avance al siguiente nivel
        if score // 10 >= nivel:
            nivel += 1
            for i in range(3):
                meteoro = Meteoro()
                all_sprites.add(meteoro)
                meteors.add(meteoro)

pygame.quit()
