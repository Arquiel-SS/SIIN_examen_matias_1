import pygame
import random
import math

# Inicializa Pygame
pygame.init()

# Configuración de la ventana
WIDTH, HEIGHT = 1250, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Juego de Recoger Pelotas")

# Carga de imágenes
def load_image(path, size):
    image = pygame.image.load(path)
    return pygame.transform.scale(image, size)

player_image = load_image("img/matias.jpg", (100, 100))
ball_image = load_image("img/monster.jpg", (36, 36))
background_image = load_image("img/fondo.jpg", (WIDTH, HEIGHT))

# Configuración del jugador
player_size = 100
initial_player_pos = [WIDTH // 2, HEIGHT // 2]
player_speed = 0.4  # Velocidad de movimiento ajustada

# Configuración de las pelotas
max_balls = 80  # Número máximo de pelotas
ball_radius = 18  # Radio de las pelotas

# Función para verificar colisión (pura)
def check_collision(player_pos, ball_pos, player_size, ball_radius):
    player_center = (player_pos[0] + player_size // 2, player_pos[1] + player_size // 2)
    ball_center = (ball_pos[0], ball_pos[1])
    distance = math.sqrt((player_center[0] - ball_center[0]) ** 2 + (player_center[1] - ball_center[1]) ** 2)
    return distance < (player_size // 2 + ball_radius)

# Función para generar una nueva posición de pelota (pura)
def generate_ball_position(ball_radius, width, height):
    return [random.randint(ball_radius, width - ball_radius), random.randint(ball_radius, height - ball_radius)]

# Función para actualizar la posición del jugador (pura)
def update_player_position(player_pos, keys, speed, width, height, size):
    new_pos = player_pos[:]
    if keys[pygame.K_LEFT] and new_pos[0] > 0:
        new_pos[0] -= speed
    if keys[pygame.K_RIGHT] and new_pos[0] < width - size:
        new_pos[0] += speed
    if keys[pygame.K_UP] and new_pos[1] > 0:
        new_pos[1] -= speed
    if keys[pygame.K_DOWN] and new_pos[1] < height - size:
        new_pos[1] += speed
    return new_pos

# Función para procesar el juego en cada frame (sin efectos colaterales)
def game_step(player_pos, balls, score, last_ball_time, max_balls, current_time, player_size, ball_radius, width, height):
    # Añadir pelotas si han pasado 500 ms
    if current_time - last_ball_time > 500 and len(balls) < max_balls:
        ball_pos = generate_ball_position(ball_radius, width, height)
        balls = balls + [ball_pos]
        last_ball_time = current_time

    # Comprobar las colisiones
    new_balls = []
    new_score = score
    for ball in balls:
        if check_collision(player_pos, ball, player_size, ball_radius):
            new_score += 1
        else:
            new_balls.append(ball)
    return new_balls, new_score, last_ball_time

# Función de dibujo de pantalla (efecto colateral de renderizado)
def draw_screen(screen, background, player_img, player_pos, ball_img, balls, score):
    screen.blit(background, (0, 0))
    screen.blit(player_img, (player_pos[0], player_pos[1]))
    for ball in balls:
        screen.blit(ball_img, (ball[0] - ball_radius, ball[1] - ball_radius))
    font = pygame.font.SysFont(None, 36)
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))
    pygame.display.flip()

# Bucle principal del programa
def main():
    player_pos = initial_player_pos[:]
    balls = []
    last_ball_time = 0
    score = 0
    running = True

    while running:
        # Manejo de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Obtener las teclas presionadas
        keys = pygame.key.get_pressed()

        # Actualizar posición del jugador
        player_pos = update_player_position(player_pos, keys, player_speed, WIDTH, HEIGHT, player_size)

        # Tiempo actual
        current_time = pygame.time.get_ticks()

        # Lógica del juego
        balls, score, last_ball_time = game_step(
            player_pos, balls, score, last_ball_time, max_balls, current_time, player_size, ball_radius, WIDTH, HEIGHT
        )

        # Dibujar la pantalla
        draw_screen(screen, background_image, player_image, player_pos, ball_image, balls, score)

    pygame.quit()

# Ejecutar el juego
if __name__ == "__main__":
    main()