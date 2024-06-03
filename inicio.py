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
RED = (255, 0, 0)
GREEN = (0, 255, 0)

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
road_image = pygame.image.load('assets/img/road.png')

player_car = scale_image(player_car, width=75)  # Ajustar el ancho del auto del jugador
enemy_car = scale_image(enemy_car, width=75)    # Ajustar el ancho del auto enemigo
road_image = scale_image(road_image, width=SCREEN_WIDTH, height=SCREEN_HEIGHT)  # Ajustar el tamaño de la carretera

# Obtener dimensiones de las imágenes redimensionadas
player_size = player_car.get_rect().size
enemy_size = enemy_car.get_rect().size

# Posición inicial del jugador
player_pos = [SCREEN_WIDTH // 2 - player_size[0] // 2, SCREEN_HEIGHT - player_size[1] - 10]

# Velocidad del jugador
player_speed = 10
player_speed_increment = 1

# Posiciones de los enemigos
enemy_pos = [random.randint(0, SCREEN_WIDTH - enemy_size[0]), 0]
enemy_speed = 10

# Incremento de velocidad de los enemigos
speed_increment = 1

# Vidas del jugador
player_lives = 3
max_lives = 5

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

# Función para mostrar un menú
def show_menu(title, options):
    selected = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    return selected

        screen.fill(BLACK)
        draw_text(title, font, WHITE, screen, SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 4)
        for i, option in enumerate(options):
            color = WHITE if i == selected else (100, 100, 100)
            draw_text(option, font, color, screen, SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + i * 50)

        pygame.display.flip()
        clock.tick(30)

# Función principal del juego
def game_loop():
    game_over = False
    paused = False
    score = 0
    global enemy_speed
    global player_speed
    global player_lives

    road_y1 = 0
    road_y2 = -SCREEN_HEIGHT

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                paused = not paused

        if not paused:
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
                enemy_speed += speed_increment  # Aumentar la velocidad de los enemigos
                if score % 10 == 0:  # Cada 10 autos adelantados
                    player_lives = min(player_lives + 1, max_lives)  # Agregar una vida extra hasta el máximo permitido
                    player_speed += player_speed_increment  # Aumentar la velocidad del jugador

            # Colisiones
            player_rect = pygame.Rect(player_pos[0], player_pos[1], player_size[0], player_size[1])
            enemy_rect = pygame.Rect(enemy_pos[0], enemy_pos[1], enemy_size[0], enemy_size[1])
            if player_rect.colliderect(enemy_rect):
                player_lives -= 1
                if player_lives == 0:
                    game_over = True
                else:
                    # Reposicionar al jugador y enemigo después de una colisión
                    player_pos[0] = SCREEN_WIDTH // 2 - player_size[0] // 2
                    player_pos[1] = SCREEN_HEIGHT - player_size[1] - 10
                    enemy_pos[0] = random.randint(0, SCREEN_WIDTH - enemy_size[0])
                    enemy_pos[1] = 0 - enemy_size[1]

            # Movimiento de la carretera
            road_y1 += enemy_speed
            road_y2 += enemy_speed
            if road_y1 >= SCREEN_HEIGHT:
                road_y1 = -SCREEN_HEIGHT
            if road_y2 >= SCREEN_HEIGHT:
                road_y2 = -SCREEN_HEIGHT

            # Dibujar en la pantalla
            screen.blit(road_image, (0, road_y1))  # Dibujar la primera imagen de la carretera
            screen.blit(road_image, (0, road_y2))  # Dibujar la segunda imagen de la carretera
            screen.blit(player_car, player_pos)
            screen.blit(enemy_car, enemy_pos)

            # Mostrar puntuación y vidas
            draw_text(f'Score: {score}', font, WHITE, screen, 10, 10)
            draw_text(f'Lives: {player_lives}', font, WHITE, screen, 10, 50)
        else:
            draw_text('Paused', font, WHITE, screen, SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 - 25)

        pygame.display.flip()
        clock.tick(30)

    return score

if __name__ == "__main__":
    while True:
        selection = show_menu("Main Menu", ["Start Game", "Quit"])
        if selection == 0:
            enemy_speed = 10  # Resetear la velocidad de los enemigos
            player_speed = 10  # Resetear la velocidad del jugador
            player_lives = 3   # Resetear las vidas del jugador
            final_score = game_loop()
            show_menu("Game Over", [f'Score: {final_score}', "Restart", "Quit"])
        elif selection == 1:
            pygame.quit()
            exit()
