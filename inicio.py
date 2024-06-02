import pygame
import random

# Inicializar pygame
pygame.init()

# Dimensiones de la pantalla
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Prueba de juego utilizando GTP')

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Función para redimensionar imágenes manteniendo la proporción
def scale_image(image, width=None, height=None):
    img_rect = image.get_rect()
    if width and height:
        return pygame.transform.scale(image, (width, height))
    elif width:
        ratio = width / img_rect.width
        return pygame.transform.scale(image, (width, int(img_rect.height * ratio)))
    elif height:
        ratio = height / img_rect.height
        return pygame.transform.scale(image, (int(img_rect.width * ratio), height))
    else:
        return image

# Cargar y redimensionar imágenes manteniendo la proporción
player_car = pygame.image.load('assets/img/player_car.png')
enemy_car = pygame.image.load('assets/img/enemy_car.png')

player_car = scale_image(player_car, width=75)  # Ajustar el ancho del auto del jugador
enemy_car = scale_image(enemy_car, width=75)    # Ajustar el ancho del auto enemigo

# Obtener dimensiones de las imágenes redimensionadas
player_size = player_car.get_rect().size
enemy_size = enemy_car.get_rect().size

# Posición inicial del jugador
player_pos = [SCREEN_WIDTH // 2 - player_size[0] // 2, SCREEN_HEIGHT - player_size[1] - 10]

# Velocidad del jugador
player_speed = 10

# Posiciones de los enemigos
enemy_pos = [random.randint(0, SCREEN_WIDTH - enemy_size[0]), 0]
enemy_speed = 10

# Reloj
clock = pygame.time.Clock()

# Fuente
font = pygame.font.SysFont("monospace", 35)

# Función para mostrar texto
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

# Función principal del juego
def game_loop():
    game_over = False
    score = 0

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

        # Movimiento del jugador
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_pos[0] > 0:
            player_pos[0] -= player_speed
        if keys[pygame.K_RIGHT] and player_pos[0] < SCREEN_WIDTH - player_size[0]:
            player_pos[0] += player_speed
        if keys[pygame.K_UP] and player_pos[1] > 0:
            player_pos[1] -= player_speed
        if keys[pygame.K_DOWN] and player_pos[1] < SCREEN_HEIGHT - player_size[1]:
            player_pos[1] += player_speed

        # Movimiento de los enemigos
        enemy_pos[1] += enemy_speed
        if enemy_pos[1] > SCREEN_HEIGHT:
            enemy_pos[0] = random.randint(0, SCREEN_WIDTH - enemy_size[0])
            enemy_pos[1] = 0 - enemy_size[1]
            score += 1

        # Colisiones
        player_rect = pygame.Rect(player_pos[0], player_pos[1], player_size[0], player_size[1])
        enemy_rect = pygame.Rect(enemy_pos[0], enemy_pos[1], enemy_size[0], enemy_size[1])
        if player_rect.colliderect(enemy_rect):
            game_over = True

        # Dibujar en la pantalla
        screen.fill(BLACK)
        screen.blit(player_car, player_pos)
        screen.blit(enemy_car, enemy_pos)

        # Mostrar puntuación
        draw_text(f'Score: {score}', font, WHITE, screen, 10, 10)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    game_loop()
